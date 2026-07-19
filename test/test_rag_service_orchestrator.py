import asyncio

from services.rag_service import RAGService


class GraphResult:
    async def ainvoke(self, initial_state, config):
        return {
            **initial_state,
            "answer": "Set LLM_API_KEY in .env.",
            "retrieved_docs": [
                {
                    "id": "knowledge/faq/mvp.jsonl",
                    "text": "Set LLM_API_KEY in .env.",
                    "source_file": "knowledge/faq/mvp.jsonl",
                    "source_path": "knowledge/faq/mvp.jsonl",
                    "score": 1.0,
                    "source_type": "faq",
                }
            ],
            "route": "faq",
            "trace": {"route": "faq"},
            "complexity": "faq",
            "retrieval_decision": {"action": "accept"},
        }

    async def astream(self, initial_state, config, stream_mode="values"):
        yield await self.ainvoke(initial_state, config)


def test_rag_service_returns_graph_result():
    service = RAGService(vector_store=None, rag_graph=GraphResult())

    result = asyncio.run(service.ask("How do I configure DashScope API Key?", session_id="s1"))

    assert result["answer"] == "Set LLM_API_KEY in .env."
    assert result["references"][0]["source_path"] == "knowledge/faq/mvp.jsonl"
    assert result["route"] == "faq"
    assert result["trace"]["route"] == "faq"
    assert result["session_id"] == "s1"


def test_rag_service_stream_returns_graph_result():
    service = RAGService(vector_store=None, rag_graph=GraphResult())

    async def collect():
        chunks = []
        async for chunk in service.ask_stream("How do I configure DashScope API Key?", session_id="s1"):
            chunks.append(chunk.decode("utf-8"))
        return "".join(chunks)

    stream = asyncio.run(collect())

    assert "event: token" in stream
    assert "event: done" in stream
    assert '"answer": "Set LLM_API_KEY in .env."' in stream
    assert '"route": "faq"' in stream
    assert "knowledge/faq/mvp.jsonl" in stream
