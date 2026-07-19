from core.agent_course_loader import build_agent_course_orchestrator


def test_build_agent_course_orchestrator_loads_faq_errors_and_code(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    faq_dir = knowledge_dir / "faq"
    errors_dir = knowledge_dir / "errors"
    courses_dir = knowledge_dir / "courses"
    code_dir = tmp_path / "src"
    faq_dir.mkdir(parents=True)
    errors_dir.mkdir(parents=True)
    courses_dir.mkdir(parents=True)
    code_dir.mkdir()

    (faq_dir / "seed.jsonl").write_text(
        '{"question":"How do I configure DashScope API Key?",'
        '"answer":"Set LLM_API_KEY in .env.",'
        '"source_path":"knowledge/faq/seed.jsonl"}\n',
        encoding="utf-8",
    )
    (errors_dir / "seed.jsonl").write_text(
        '{"error_pattern":"ModuleNotFoundError: No module named pymilvus",'
        '"symptom":"Import fails",'
        '"cause":"pymilvus is not installed",'
        '"fix_steps":["Run pip install -r requirements.txt"],'
        '"source_path":"knowledge/errors/seed.jsonl"}\n',
        encoding="utf-8",
    )
    (code_dir / "sample.py").write_text(
        "def target_function():\n"
        "    return 'ok'\n",
        encoding="utf-8",
    )
    (courses_dir / "rag-basics.md").write_text(
        "# RAG basics\n"
        "Retrieval augmented generation retrieves evidence before generation.\n",
        encoding="utf-8",
    )

    orchestrator = build_agent_course_orchestrator(
        knowledge_dir=knowledge_dir,
        code_roots=str(code_dir),
    )

    assert len(orchestrator.faqs) == 1
    assert len(orchestrator.error_recipes) == 1
    assert len(orchestrator.course_docs) == 1
    assert [symbol.symbol_name for symbol in orchestrator.code_symbols] == ["target_function"]

    faq = orchestrator.answer("How do I configure DashScope API Key?")
    assert faq.route == "faq"
    assert "LLM_API_KEY" in faq.answer

    code = orchestrator.answer("Where is target_function in sample.py?")
    assert code.route == "code"
    assert code.citations[0]["source_type"] == "project_code"

    course = orchestrator.answer("What is retrieval augmented generation?")
    assert course.route == "course"
    assert course.citations[0]["source_type"] == "course_note"


def test_course_loader_reads_basic_front_matter_acl(tmp_path):
    from core.agent_course_loader import load_course_docs

    knowledge_dir = tmp_path / "knowledge"
    courses_dir = knowledge_dir / "courses"
    courses_dir.mkdir(parents=True)
    (courses_dir / "private.md").write_text(
        "---\n"
        "visibility: private\n"
        "allowed_users: [u1, u2]\n"
        "source_type: course_note\n"
        "---\n"
        "# Private lesson\n"
        "Agent memory uses scoped state.\n",
        encoding="utf-8",
    )

    docs = load_course_docs(knowledge_dir)

    assert docs[0]["visibility"] == "private"
    assert docs[0]["allowed_users"] == ["u1", "u2"]
    assert docs[0]["source_type"] == "course_note"
