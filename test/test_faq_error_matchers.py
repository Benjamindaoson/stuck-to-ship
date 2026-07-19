def test_match_faq_direct_answer_keeps_source_path():
    from core.faq_matcher import match_faq

    result = match_faq(
        "How do I configure DashScope API Key?",
        [
            {
                "question": "How do I configure DashScope API Key?",
                "answer": "Set LLM_API_KEY in .env.",
                "source_path": "knowledge/faq/mvp.jsonl",
            }
        ],
        threshold=0.5,
    )

    assert result["answer"].startswith("Set LLM_API_KEY")
    assert result["source_path"] == "knowledge/faq/mvp.jsonl"


def test_match_error_recipe_by_pattern_keeps_source_path():
    from core.error_matcher import match_error_recipe

    result = match_error_recipe(
        "ModuleNotFoundError: No module named 'pymilvus'",
        [
            {
                "error_pattern": "ModuleNotFoundError",
                "cause": "missing dependency",
                "fix_steps": ["pip install pymilvus"],
                "source_path": "knowledge/errors/mvp.jsonl",
            }
        ],
    )

    assert result["cause"] == "missing dependency"
    assert result["source_path"] == "knowledge/errors/mvp.jsonl"
