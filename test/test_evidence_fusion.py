from core.retrieval.contracts import EvidenceCandidate


def candidate(evidence_id: str, strategy: str, score_name: str, score: float) -> EvidenceCandidate:
    return EvidenceCandidate(
        id=evidence_id,
        text=f"{strategy} text",
        source_path="knowledge/courses/rag.md",
        source_type="course_note",
        modality="text",
        location={"start_line": 1, "end_line": 2},
        raw_scores={score_name: score},
        retrieval_strategy=strategy,
        metadata={strategy: True},
    )


def test_fusion_deduplicates_by_stable_identity_and_preserves_raw_scores():
    from core.retrieval.engine import fuse_candidates

    fused = fuse_candidates(
        [
            candidate("knowledge/courses/rag.md:1-2", "dense", "dense", 0.82),
            candidate("knowledge/courses/rag.md:1-2", "sparse", "sparse", 3.4),
        ]
    )

    assert len(fused) == 1
    assert fused[0].id == "knowledge/courses/rag.md:1-2"
    assert fused[0].raw_scores == {"dense": 0.82, "sparse": 3.4}
    assert fused[0].retrieval_strategy == "dense+sparse"
    assert fused[0].metadata == {"dense": True, "sparse": True}


def test_fusion_order_is_deterministic_by_score_then_identity():
    from core.retrieval.engine import fuse_candidates

    fused = fuse_candidates(
        [
            candidate("b", "dense", "dense", 0.7),
            candidate("a", "dense", "dense", 0.7),
            candidate("c", "sparse", "sparse", 1.1),
        ]
    )

    assert [item.id for item in fused] == ["c", "a", "b"]
