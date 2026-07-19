import asyncio

from core.qa_orchestrator import QAResult
from services.rag_service import RAGService


class ShouldNotRunGraph:
    async def ainvoke(self, *args, **kwargs):
        raise AssertionError("LangGraph path should not run for orchestrator-routed answers")


class StubOrchestrator:
    def answer(self, query, session_id=None, user_id=None):
        return QAResult(
            answer="请补充具体课程、代码文件或报错信息。",
            route="clarify",
            citations=[],
            trace={
                "query": query,
                "session_id": session_id,
                "route": "clarify",
                "decision": "clarify",
                "latency_ms": 0,
            },
            needs_clarification=True,
        )


class StubCitationOrchestrator:
    def answer(self, query, session_id=None, user_id=None):
        return QAResult(
            answer="Set LLM_API_KEY in .env.",
            route="faq",
            citations=[
                {
                    "source_path": "knowledge/faq/mvp.jsonl",
                    "title": "FAQ",
                    "source_type": "faq",
                    "start_line": None,
                    "end_line": None,
                    "score": 1.0,
                }
            ],
            trace={
                "query": query,
                "session_id": session_id,
                "route": "faq",
                "decision": "accept",
                "latency_ms": 0,
            },
            needs_clarification=False,
        )


def test_rag_service_returns_orchestrator_result_before_langgraph():
    service = RAGService(
        vector_store=None,
        rag_graph=ShouldNotRunGraph(),
        qa_orchestrator=StubOrchestrator(),
    )

    result = asyncio.run(service.ask("这个怎么弄？", session_id="s1"))

    assert result["answer"] == "请补充具体课程、代码文件或报错信息。"
    assert result["references"] == []
    assert result["route"] == "clarify"
    assert result["trace"]["decision"] == "clarify"
    assert result["session_id"] == "s1"


def test_rag_service_stream_returns_orchestrator_result_before_langgraph():
    service = RAGService(
        vector_store=None,
        rag_graph=ShouldNotRunGraph(),
        qa_orchestrator=StubCitationOrchestrator(),
    )

    async def collect():
        chunks = []
        async for chunk in service.ask_stream("How do I configure DashScope API Key?", session_id="s1"):
            chunks.append(chunk.decode("utf-8"))
        return "".join(chunks)

    stream = asyncio.run(collect())

    assert "event: done" in stream
    assert '"answer": "Set LLM_API_KEY in .env."' in stream
    assert '"route": "faq"' in stream
    assert "knowledge/faq/mvp.jsonl" in stream
