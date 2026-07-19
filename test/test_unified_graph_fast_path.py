import asyncio
from unittest.mock import AsyncMock, patch


class ShouldNotSearchStore:
    def hybrid_search(self, **kwargs):
        raise AssertionError("fast path should not call vector search")


class ShouldNotRerank:
    async def rerank(self, query, docs):
        raise AssertionError("fast path should not call reranker")


def test_graph_faq_fast_path_finalizes_cited_answer_without_llm():
    from core.graph import build_rag_graph
    from core.qa_orchestrator import QAOrchestrator

    graph = build_rag_graph(
        ShouldNotSearchStore(),
        ShouldNotRerank(),
        qa_orchestrator=QAOrchestrator(
            faqs=[
                {
                    "question": "How do I configure API key?",
                    "answer": "Set LLM_API_KEY in your local environment.",
                    "source_path": "knowledge/faq/mvp.jsonl",
                }
            ]
        ),
        checkpointer=False,
    )

    with (
        patch("core.graph.classify_intent_async", new=AsyncMock(return_value="educational")),
        patch("core.graph.classify_query_with_fallback", new=AsyncMock(return_value="simple")),
        patch("core.graph.llm_generate_stream", new=AsyncMock(side_effect=AssertionError("LLM must not run"))),
    ):
        final_state = asyncio.run(graph.ainvoke(_initial_state("How do I configure API key?")))

    assert final_state["answer"] == "Set LLM_API_KEY in your local environment."
    assert final_state["route"] == "faq"
    assert final_state["retrieval_decision"]["action"] == "accept"
    assert final_state["retrieved_docs"][0]["source_path"] == "knowledge/faq/mvp.jsonl"
    assert final_state["conversation_history"][-1]["content"] == "Set LLM_API_KEY in your local environment."


def test_graph_exact_faq_fast_path_runs_before_intent_classifier():
    from core.graph import build_rag_graph
    from core.qa_orchestrator import QAOrchestrator

    graph = build_rag_graph(
        ShouldNotSearchStore(),
        ShouldNotRerank(),
        qa_orchestrator=QAOrchestrator(
            faqs=[
                {
                    "question": "How do I configure API key?",
                    "answer": "Set LLM_API_KEY in your local environment.",
                    "source_path": "knowledge/faq/mvp.jsonl",
                }
            ]
        ),
        checkpointer=False,
    )

    with patch("core.graph.classify_intent_async", new=AsyncMock(side_effect=AssertionError("classifier must not run"))):
        final_state = asyncio.run(graph.ainvoke(_initial_state("How do I configure API key?")))

    assert final_state["route"] == "faq"
    assert final_state["answer"] == "Set LLM_API_KEY in your local environment."


def test_graph_clarify_fast_path_finalizes_without_retrieval_gate_acceptance():
    from core.graph import build_rag_graph
    from core.qa_orchestrator import QAOrchestrator

    graph = build_rag_graph(
        ShouldNotSearchStore(),
        ShouldNotRerank(),
        qa_orchestrator=QAOrchestrator(),
        checkpointer=False,
    )

    with (
        patch("core.graph.classify_intent_async", new=AsyncMock(return_value="educational")),
        patch("core.graph.classify_query_with_fallback", new=AsyncMock(return_value="simple")),
    ):
        final_state = asyncio.run(graph.ainvoke(_initial_state("help")))

    assert final_state["route"] == "clarify"
    assert final_state["retrieval_decision"]["action"] == "clarify"
    assert final_state["retrieved_docs"] == []
    assert "course topic" in final_state["answer"]


def test_app_state_injects_orchestrator_into_graph(monkeypatch):
    import main

    vector_store = object()
    orchestrator = object()
    graph = object()
    captured = {}

    def fake_init_rag_graph_sync(received_vector_store, received_orchestrator=None):
        captured["vector_store"] = received_vector_store
        captured["orchestrator"] = received_orchestrator
        return graph

    monkeypatch.setattr(main, "init_rag_graph_sync", fake_init_rag_graph_sync)

    state = main.build_app_state(vector_store=vector_store, qa_orchestrator=orchestrator)

    assert state.rag_graph is graph
    assert captured == {"vector_store": vector_store, "orchestrator": orchestrator}


def _initial_state(query: str) -> dict:
    return {
        "query": query,
        "subject": None,
        "grade": None,
        "session_id": "session-1",
        "intent": "",
        "complexity": "",
        "retrieved_docs": [],
        "answer": "",
        "retry_count": 0,
        "max_retries": 0,
        "conversation_history": [],
        "retrieval_plan": {"strategy": "initial", "queries": [query]},
        "retrieval_attempts": [],
        "retrieval_metrics": {},
        "retrieval_decision": {},
        "abstain_reason": "",
        "sub_queries": [],
        "_queue_id": "",
    }
