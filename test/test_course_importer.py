import json
from pathlib import Path


def test_import_course_assets_copies_lessons_and_validates_jsonl(tmp_path):
    from ingestion.course_importer import import_course_assets

    source = tmp_path / "source"
    (source / "courses").mkdir(parents=True)
    (source / "faq").mkdir()
    (source / "errors").mkdir()
    (source / "eval").mkdir()
    (source / "courses" / "rag.md").write_text("# RAG\nUse retrieval before generation.\n", encoding="utf-8")
    (source / "faq" / "faq.jsonl").write_text(
        json.dumps({"question": "How to set API key?", "answer": "Set LLM_API_KEY."}) + "\n",
        encoding="utf-8",
    )
    (source / "errors" / "errors.jsonl").write_text(
        json.dumps(
            {
                "error_pattern": "ModuleNotFoundError",
                "symptom": "import fails",
                "cause": "missing package",
                "fix_steps": ["pip install -r requirements.txt"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (source / "eval" / "manual.jsonl").write_text(
        json.dumps({"question": "What is RAG?", "expected_route": "course", "should_answer": True}) + "\n",
        encoding="utf-8",
    )

    target = tmp_path / "project"
    report = import_course_assets(source, target)

    assert report["courses"] == 1
    assert report["faq"] == 1
    assert report["errors"] == 1
    assert report["eval"] == 1
    assert (target / "knowledge" / "courses" / "rag.md").exists()
    assert (target / "knowledge" / "faq" / "faq.jsonl").exists()
    assert (target / "knowledge" / "errors" / "errors.jsonl").exists()
    assert (target / "data" / "agent_course_eval" / "manual.jsonl").exists()
    assert (target / "knowledge" / "course_manifest.json").exists()


def test_import_course_assets_rejects_invalid_faq_jsonl(tmp_path):
    from ingestion.course_importer import import_course_assets

    source = tmp_path / "source"
    (source / "faq").mkdir(parents=True)
    (source / "faq" / "bad.jsonl").write_text(json.dumps({"question": "missing answer"}) + "\n", encoding="utf-8")

    try:
        import_course_assets(source, tmp_path / "project")
    except ValueError as exc:
        assert "faq" in str(exc)
        assert "answer" in str(exc)
    else:
        raise AssertionError("invalid FAQ JSONL should fail")
