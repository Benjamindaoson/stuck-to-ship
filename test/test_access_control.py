def test_private_course_evidence_requires_allowed_user():
    from core.qa_orchestrator import QAOrchestrator

    orchestrator = QAOrchestrator(
        course_docs=[
            {
                "title": "Private Agent lesson",
                "text": "Agent memory uses scoped state and tool traces.",
                "source_path": "knowledge/courses/private-agent.md",
                "source_type": "course_note",
                "visibility": "private",
                "allowed_users": ["u1"],
            }
        ]
    )

    blocked = orchestrator.answer("How does Agent memory work?", user_id="u2")
    allowed = orchestrator.answer("How does Agent memory work?", user_id="u1")

    assert blocked.citations == []
    assert blocked.trace["decision"] == "clarify_or_refuse"
    assert blocked.trace["blocked_evidence"][0]["reason"] == "acl_denied"
    assert allowed.citations
    assert allowed.citations[0]["source_path"].endswith("private-agent.md")
