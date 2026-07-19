def test_orchestrator_clarifies_ambiguous_question():
    from core.qa_orchestrator import QAOrchestrator

    result = QAOrchestrator().answer("这个怎么弄？")
    assert result.needs_clarification is True
    assert result.route == "clarify"


def test_orchestrator_returns_citation_for_code_question(tmp_path):
    sample = tmp_path / "main.py"
    sample.write_text("def create_app():\n    return 'app'\n", encoding="utf-8")

    from ingestion.code_indexer import extract_python_symbols
    from core.qa_orchestrator import QAOrchestrator

    orchestrator = QAOrchestrator(code_symbols=extract_python_symbols(tmp_path))
    result = orchestrator.answer("create_app 在哪里？")
    assert result.route == "code"
    assert result.citations
    assert result.citations[0]["source_path"].endswith("main.py")


def test_orchestrator_returns_course_citation():
    from core.qa_orchestrator import QAOrchestrator

    orchestrator = QAOrchestrator(
        course_docs=[
            {
                "title": "RAG basics",
                "text": "Retrieval augmented generation retrieves course evidence before generation.",
                "source_path": "knowledge/courses/rag-basics.md",
                "source_type": "course_note",
                "start_line": 1,
                "end_line": 2,
            }
        ]
    )

    result = orchestrator.answer("What is retrieval augmented generation in LLM applications?")

    assert result.route == "course"
    assert result.citations
    assert result.citations[0]["source_type"] == "course_note"
    assert result.needs_clarification is False


def test_orchestrator_returns_learning_path_citation():
    from core.qa_orchestrator import QAOrchestrator

    orchestrator = QAOrchestrator(
        course_docs=[
            {
                "title": "Agent learning path",
                "text": "After vector retrieval, study reranking, evaluation, LangGraph, tool calling, and MCP.",
                "source_path": "knowledge/courses/agent-learning-path.md",
                "source_type": "course_outline",
                "start_line": 1,
                "end_line": 2,
            }
        ]
    )

    result = orchestrator.answer("我学完向量检索后下一步做什么？")

    assert result.route == "learning_path"
    assert result.citations
    assert "reranking" in result.answer
