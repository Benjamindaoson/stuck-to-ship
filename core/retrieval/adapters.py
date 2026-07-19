from __future__ import annotations

from core.code_retriever import search_code_symbols
from core.course_retriever import search_course_docs
from core.error_matcher import match_error_recipe
from core.faq_matcher import match_faq
from core.retrieval.contracts import EvidenceCandidate, RetrievalQuery
from ingestion.code_indexer import CodeSymbol


SECURITY_METADATA_KEYS = {
    "visibility",
    "allowed_users",
    "owner_id",
    "acl",
    "injection_checked",
    "safety_flags",
}


class CourseRetrieverAdapter:
    def __init__(self, docs: list[dict]):
        self.docs = docs

    async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
        results = search_course_docs(query.text, self.docs, route=query.route)
        return [_course_candidate(item) for item in results]


class CodeRetrieverAdapter:
    def __init__(self, symbols: list[CodeSymbol]):
        self.symbols = symbols

    async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
        results = search_code_symbols(query.text, self.symbols)
        return [_code_candidate(item) for item in results]


class FAQRetrieverAdapter:
    def __init__(self, faqs: list[dict]):
        self.faqs = faqs

    async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
        item = match_faq(query.text, self.faqs, threshold=0.58)
        return [_faq_candidate(item)] if item else []


class ErrorRetrieverAdapter:
    def __init__(self, recipes: list[dict]):
        self.recipes = recipes

    async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
        item = match_error_recipe(query.text, self.recipes)
        return [_error_candidate(item)] if item else []


def _course_candidate(item: dict) -> EvidenceCandidate:
    start = item.get("start_line")
    end = item.get("end_line")
    source_path = str(item.get("source_path") or "")
    return EvidenceCandidate(
        id=_line_id(source_path, start, end),
        text=str(item.get("text") or ""),
        source_path=source_path,
        source_type=str(item.get("source_type") or "course_note"),
        modality="text",
        location=_line_location(start, end),
        raw_scores={"course": float(item.get("score") or 0.0)},
        retrieval_strategy="course",
        metadata=_metadata(item, extra_keys={"title"}),
    )


def _code_candidate(item: dict) -> EvidenceCandidate:
    start = item.get("start_line")
    end = item.get("end_line")
    source_path = str(item.get("source_path") or "")
    symbol_name = str(item.get("symbol_name") or "")
    return EvidenceCandidate(
        id=f"{_line_id(source_path, start, end)}:{symbol_name}",
        text=str(item.get("text") or ""),
        source_path=source_path,
        source_type=str(item.get("source_type") or "project_code"),
        modality="code",
        location=_line_location(start, end),
        raw_scores={"exact": float(item.get("score") or 0.0)},
        retrieval_strategy="code",
        metadata=_metadata(item, extra_keys={"symbol_name", "symbol_type"}),
    )


def _faq_candidate(item: dict) -> EvidenceCandidate:
    source_path = str(item.get("source_path") or "faq")
    question = str(item.get("question") or "")
    return EvidenceCandidate(
        id=f"{source_path}:faq:{question}",
        text=str(item.get("answer") or item.get("text") or ""),
        source_path=source_path,
        source_type=str(item.get("source_type") or "faq"),
        modality="text",
        location={},
        raw_scores={"faq": float(item.get("score") or 0.0)},
        retrieval_strategy="faq",
        metadata=_metadata(item, extra_keys={"question"}),
    )


def _error_candidate(item: dict) -> EvidenceCandidate:
    source_path = str(item.get("source_path") or "errors")
    pattern = str(item.get("error_pattern") or "")
    text = " ".join(
        str(part)
        for part in [
            item.get("error_pattern", ""),
            item.get("symptom", ""),
            item.get("cause", ""),
            item.get("fix_steps", ""),
            item.get("verify_command", ""),
        ]
    )
    return EvidenceCandidate(
        id=f"{source_path}:error:{pattern}",
        text=text,
        source_path=source_path,
        source_type=str(item.get("source_type") or "error_recipe"),
        modality="text",
        location={},
        raw_scores={"error": float(item.get("score") or 0.0)},
        retrieval_strategy="error",
        metadata=_metadata(item, extra_keys={"error_pattern", "cause", "fix_steps", "verify_command"}),
    )


def _line_id(source_path: str, start: object, end: object) -> str:
    if start and end:
        return f"{source_path}:{start}-{end}"
    if start:
        return f"{source_path}:{start}"
    return source_path


def _line_location(start: object, end: object) -> dict[str, int | float | str]:
    location: dict[str, int | float | str] = {}
    if start is not None:
        location["start_line"] = start
    if end is not None:
        location["end_line"] = end
    return location


def _metadata(item: dict, *, extra_keys: set[str]) -> dict[str, object]:
    keys = SECURITY_METADATA_KEYS | extra_keys
    return {key: item[key] for key in keys if key in item}
