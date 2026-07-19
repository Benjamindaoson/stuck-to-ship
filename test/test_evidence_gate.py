def test_gate_accepts_supported_answer():
    from core.evidence import build_evidence_packet
    from core.retrieval_gate import decide_evidence

    packet = build_evidence_packet(
        "RAG 是什么？",
        [{"text": "RAG 通过检索外部知识增强回答。", "score": 0.82, "source_path": "lesson.md"}],
    )
    decision = decide_evidence(packet)
    assert decision.action == "accept"


def test_gate_refuses_low_evidence():
    from core.evidence import build_evidence_packet
    from core.retrieval_gate import decide_evidence

    packet = build_evidence_packet("RAG 是什么？", [])
    decision = decide_evidence(packet)
    assert decision.action == "clarify_or_refuse"
