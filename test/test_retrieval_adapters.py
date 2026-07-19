import asyncio

from core.retrieval.contracts import RetrievalQuery
from ingestion.code_indexer import CodeSymbol


def test_course_adapter_normalizes_source_lines_scores_and_security_metadata():
    from core.retrieval.adapters import CourseRetrieverAdapter

    adapter = CourseRetrieverAdapter(
        [
            {
                "title": "Agent memory",
                "text": "Agent memory uses scoped state, summaries, and retrieval.",
                "source_path": "knowledge/courses/agent-memory.md",
                "source_type": "course_note",
                "start_line": 7,
                "end_line": 9,
                "visibility": "private",
                "allowed_users": ["u1"],
                "injection_checked": True,
            }
        ]
    )

    results = asyncio.run(
        adapter.retrieve(RetrievalQuery(text="How does Agent memory work?", route="course", user_id="u1"))
    )

    assert len(results) == 1
    candidate = results[0]
    assert candidate.id == "knowledge/courses/agent-memory.md:7-9"
    assert candidate.source_path == "knowledge/courses/agent-memory.md"
    assert candidate.source_type == "course_note"
    assert candidate.modality == "text"
    assert candidate.location == {"start_line": 7, "end_line": 9}
    assert candidate.raw_scores["course"] >= 0.45
    assert candidate.metadata["visibility"] == "private"
    assert candidate.metadata["allowed_users"] == ["u1"]
    assert candidate.metadata["injection_checked"] is True


def test_code_adapter_normalizes_symbol_location_and_exact_score():
    from core.retrieval.adapters import CodeRetrieverAdapter

    adapter = CodeRetrieverAdapter(
        [
            CodeSymbol(
                source_path="services/rag_service.py",
                symbol_name="ask",
                symbol_type="function",
                start_line=101,
                end_line=170,
                text="async def ask(...):\n    pass",
            )
        ]
    )

    results = asyncio.run(
        adapter.retrieve(RetrievalQuery(text="Where is ask function defined?", route="code"))
    )

    assert results[0].id == "services/rag_service.py:101-170:ask"
    assert results[0].modality == "code"
    assert results[0].location == {"start_line": 101, "end_line": 170}
    assert results[0].raw_scores["exact"] == 2.5
    assert results[0].metadata["symbol_name"] == "ask"
    assert results[0].metadata["symbol_type"] == "function"


def test_faq_adapter_normalizes_answer_source_and_score():
    from core.retrieval.adapters import FAQRetrieverAdapter

    adapter = FAQRetrieverAdapter(
        [
            {
                "question": "How do I configure API key?",
                "answer": "Set LLM_API_KEY in your local environment.",
                "source_path": "knowledge/faq/mvp.jsonl",
                "injection_checked": True,
            }
        ]
    )

    results = asyncio.run(
        adapter.retrieve(RetrievalQuery(text="How do I configure API key?", route="faq"))
    )

    assert results[0].id == "knowledge/faq/mvp.jsonl:faq:How do I configure API key?"
    assert results[0].text == "Set LLM_API_KEY in your local environment."
    assert results[0].source_type == "faq"
    assert results[0].raw_scores["faq"] == 1.0
    assert results[0].metadata["question"] == "How do I configure API key?"
    assert results[0].metadata["injection_checked"] is True


def test_error_adapter_normalizes_recipe_source_and_fix_metadata():
    from core.retrieval.adapters import ErrorRetrieverAdapter

    adapter = ErrorRetrieverAdapter(
        [
            {
                "error_pattern": "ModuleNotFoundError",
                "cause": "The package is missing from .venv.",
                "fix_steps": ["Install requirements", "Retry command"],
                "source_path": "knowledge/errors/mvp.jsonl",
            }
        ]
    )

    results = asyncio.run(
        adapter.retrieve(
            RetrievalQuery(text="ModuleNotFoundError: No module named langgraph", route="error")
        )
    )

    assert results[0].id == "knowledge/errors/mvp.jsonl:error:ModuleNotFoundError"
    assert results[0].source_type == "error_recipe"
    assert results[0].raw_scores["error"] == 1.0
    assert results[0].metadata["cause"] == "The package is missing from .venv."
    assert results[0].metadata["fix_steps"] == ["Install requirements", "Retry command"]
