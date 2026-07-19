from __future__ import annotations

import time
from dataclasses import dataclass, field

from core.code_retriever import search_code_symbols
from core.course_retriever import search_course_docs
from core.error_matcher import match_error_recipe
from core.evidence import build_evidence_packet
from core.faq_matcher import match_faq
from core.intent_router import route_query
from core.retrieval_gate import decide_evidence
from ingestion.code_indexer import CodeSymbol


@dataclass(frozen=True)
class QAResult:
    answer: str
    route: str
    citations: list[dict] = field(default_factory=list)
    trace: dict = field(default_factory=dict)
    needs_clarification: bool = False


class QAOrchestrator:
    def __init__(
        self,
        *,
        code_symbols: list[CodeSymbol] | None = None,
        course_docs: list[dict] | None = None,
        faqs: list[dict] | None = None,
        error_recipes: list[dict] | None = None,
    ):
        self.code_symbols = code_symbols or []
        self.course_docs = course_docs or []
        self.faqs = faqs or []
        self.error_recipes = error_recipes or []

    def answer(
        self,
        query: str,
        session_id: str | None = None,
        user_id: str | None = None,
    ) -> QAResult:
        started = time.perf_counter()
        route = route_query(query)
        prefetched_error = match_error_recipe(query, self.error_recipes)
        prefetched_faq = match_faq(query, self.faqs, threshold=0.58)
        if prefetched_error:
            route = type(route)("error", 0.95, "matched_error_recipe")
        elif prefetched_faq and route.route == "course":
            route = type(route)("faq", 0.9, "matched_faq_record")
        candidates = self._retrieve(
            query,
            route.route,
            prefetched_faq=prefetched_faq,
            prefetched_error=prefetched_error,
        )
        packet = build_evidence_packet(query, candidates, user_id=user_id)
        gate = decide_evidence(packet)
        citations = [_citation(item) for item in packet.evidence]

        if route.needs_clarification:
            answer = "Please add the course topic, code file, full error, or concept you want explained."
            needs_clarification = True
        elif gate.action == "accept":
            answer = self._grounded_answer(route.route, candidates)
            needs_clarification = False
        else:
            answer = (
                "I do not have enough cited evidence to answer this reliably. "
                "Add a course chapter, code file, full error, or runtime context."
            )
            needs_clarification = gate.action in {"clarify_or_refuse", "retry"}

        trace = {
            "query": query,
            "session_id": session_id or "",
            "route": route.route,
            "route_reason": route.reason,
            "decision": gate.action if not route.needs_clarification else "clarify",
            "candidates": candidates,
            "blocked_evidence": packet.blocked_evidence,
            "citations": citations,
            "latency_ms": int((time.perf_counter() - started) * 1000),
        }
        return QAResult(
            answer=answer,
            route=route.route,
            citations=citations,
            trace=trace,
            needs_clarification=needs_clarification,
        )

    def _retrieve(
        self,
        query: str,
        route: str,
        *,
        prefetched_faq: dict | None = None,
        prefetched_error: dict | None = None,
    ) -> list[dict]:
        if route == "code":
            return search_code_symbols(query, self.code_symbols)
        if route == "faq":
            item = prefetched_faq or match_faq(query, self.faqs, threshold=0.58)
            return [_faq_candidate(item)] if item else []
        if route == "error":
            item = prefetched_error or match_error_recipe(query, self.error_recipes)
            return [_error_candidate(item)] if item else []
        if route in {"course", "learning_path"}:
            return search_course_docs(query, self.course_docs, route=route)
        return []

    @staticmethod
    def _grounded_answer(route: str, candidates: list[dict]) -> str:
        if route == "code" and candidates:
            item = candidates[0]
            return f"{item.get('symbol_name')} is in {item.get('source_path')}:{item.get('start_line')}."
        if route == "faq" and candidates:
            return str(candidates[0].get("answer") or candidates[0].get("text") or "")
        if route == "error" and candidates:
            item = candidates[0]
            steps = item.get("fix_steps") or []
            if isinstance(steps, list):
                steps = "; ".join(str(step) for step in steps)
            return f"Likely cause: {item.get('cause', '')}. Fix: {steps}"
        if route in {"course", "learning_path"} and candidates:
            return _course_answer(candidates)
        return "I found relevant evidence. Check the cited sources for details."


def _citation(evidence) -> dict:
    return {
        "source_path": evidence.source_path,
        "source_file": evidence.source_path,
        "title": evidence.title,
        "source_type": evidence.source_type,
        "start_line": evidence.start_line,
        "end_line": evidence.end_line,
        "score": evidence.score,
        "text": evidence.text,
    }


def _faq_candidate(item: dict | None) -> dict:
    if not item:
        return {}
    return {
        **item,
        "text": item.get("answer", ""),
        "source_path": item.get("source_path", "faq"),
        "score": item.get("score", 1.0),
    }


def _error_candidate(item: dict | None) -> dict:
    if not item:
        return {}
    return {
        **item,
        "text": " ".join(
            str(part)
            for part in [
                item.get("error_pattern", ""),
                item.get("symptom", ""),
                item.get("cause", ""),
                item.get("fix_steps", ""),
                item.get("verify_command", ""),
            ]
        ),
        "source_path": item.get("source_path", "errors"),
        "score": item.get("score", 1.0),
    }


def _course_answer(candidates: list[dict]) -> str:
    lines = []
    for item in candidates[:3]:
        title = str(item.get("title") or item.get("source_path") or "course note")
        text = " ".join(str(item.get("text") or "").split())
        if len(text) > 420:
            text = text[:417] + "..."
        lines.append(f"- {title}: {text}")
    return "Based on the course evidence:\n" + "\n".join(lines)
