import pytest


def test_retrieval_query_is_frozen_and_carries_filters():
    from core.retrieval.contracts import RetrievalQuery

    query = RetrievalQuery(
        text="Explain LangGraph retries.",
        route="course",
        user_id="u1",
        filters={"course": "agent"},
    )

    assert query.text == "Explain LangGraph retries."
    assert query.filters["course"] == "agent"
    with pytest.raises(Exception):
        query.route = "faq"


def test_evidence_candidate_preserves_identity_location_scores_and_security_metadata():
    from core.retrieval.contracts import EvidenceCandidate

    candidate = EvidenceCandidate(
        id="knowledge/courses/langgraph.md:12-18",
        text="LangGraph retries route failed retrieval through a corrective node.",
        source_path="knowledge/courses/langgraph.md",
        source_type="course_note",
        modality="text",
        location={"start_line": 12, "end_line": 18},
        raw_scores={"dense": 0.81, "sparse": 4.2},
        retrieval_strategy="hybrid",
        metadata={"visibility": "public", "injection_checked": True},
    )

    assert candidate.id == "knowledge/courses/langgraph.md:12-18"
    assert candidate.location["start_line"] == 12
    assert candidate.raw_scores["dense"] == 0.81
    assert candidate.metadata["injection_checked"] is True
    with pytest.raises(Exception):
        candidate.source_path = "other.md"


def test_retriever_protocol_accepts_async_retrievers():
    from core.retrieval.contracts import EvidenceCandidate, RetrievalQuery, Retriever

    class DummyRetriever:
        async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
            return [
                EvidenceCandidate(
                    id="faq:api-key",
                    text="Set LLM_API_KEY in the project environment.",
                    source_path="knowledge/faq/mvp.jsonl",
                    source_type="faq",
                    modality="text",
                    location={},
                    raw_scores={"exact": 1.0},
                    retrieval_strategy="faq",
                    metadata={},
                )
            ]

    assert isinstance(DummyRetriever(), Retriever)
