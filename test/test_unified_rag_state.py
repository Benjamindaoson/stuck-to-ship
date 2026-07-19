from typing import get_type_hints


def test_rag_state_declares_unified_retrieval_fields():
    from core.state import RAGState

    hints = get_type_hints(RAGState)

    for field in [
        "normalized_evidence",
        "selected_tools",
        "planner_budget",
        "gate_decision",
        "citations",
        "redacted_trace",
    ]:
        assert field in hints
