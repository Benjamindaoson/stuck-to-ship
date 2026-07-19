import asyncio


class ExplodingOrchestrator:
    def answer(self, *args, **kwargs):
        raise AssertionError("RAGService should not call QAOrchestrator directly")


class FastPathGraph:
    async def ainvoke(self, initial_state, config):
        return {
            **initial_state,
            "answer": "Set LLM_API_KEY in your local environment.",
            "retrieved_docs": [
                {
                    "id": "knowledge/faq/mvp.jsonl",
                    "text": "Set LLM_API_KEY in your local environment.",
                    "source_path": "knowledge/faq/mvp.jsonl",
                    "source_file": "knowledge/faq/mvp.jsonl",
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


def test_service_non_streaming_uses_graph_as_single_answer_path():
    from services.rag_service import RAGService

    service = RAGService(None, FastPathGraph(), qa_orchestrator=ExplodingOrchestrator())

    result = asyncio.run(service.ask("How do I configure API key?", session_id="s1"))

    assert result["answer"] == "Set LLM_API_KEY in your local environment."
    assert result["route"] == "faq"
    assert result["references"][0]["source_path"] == "knowledge/faq/mvp.jsonl"


def test_service_streaming_uses_graph_as_single_answer_path():
    from services.rag_service import RAGService

    service = RAGService(None, FastPathGraph(), qa_orchestrator=ExplodingOrchestrator())

    async def collect():
        chunks = []
        async for chunk in service.ask_stream("How do I configure API key?", session_id="s1"):
            chunks.append(chunk.decode("utf-8"))
        return "".join(chunks)

    stream = asyncio.run(collect())

    assert "event: done" in stream
    assert '"answer": "Set LLM_API_KEY in your local environment."' in stream
    assert '"session_id": "s1"' in stream
