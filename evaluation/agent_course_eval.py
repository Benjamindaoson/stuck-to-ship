from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Protocol

from core.qa_orchestrator import QAOrchestrator, QAResult


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_PATH = PROJECT_ROOT / "data" / "agent_course_eval" / "manual_v1.jsonl"
VALID_ROUTES = {"course", "code", "error", "faq", "learning_path", "clarify"}


class Answerer(Protocol):
    def answer(self, query: str, session_id: str | None = None) -> QAResult:
        ...


@dataclass(frozen=True)
class AgentCourseEvalCase:
    id: str
    question: str
    expected_route: str
    target_behavior: str
    expected_source_types: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: dict, line_no: int) -> "AgentCourseEvalCase":
        required = ["id", "question", "expected_route", "target_behavior"]
        missing = [key for key in required if not data.get(key)]
        if missing:
            raise ValueError(f"line {line_no}: missing required fields: {', '.join(missing)}")
        route = str(data["expected_route"])
        if route not in VALID_ROUTES:
            raise ValueError(f"line {line_no}: unsupported expected_route: {route}")
        return cls(
            id=str(data["id"]),
            question=str(data["question"]),
            expected_route=route,
            target_behavior=str(data["target_behavior"]),
            expected_source_types=tuple(data.get("expected_source_types") or ()),
            tags=tuple(data.get("tags") or ()),
        )


def resolve_eval_path(path: str | Path | None = None) -> Path:
    if path is None:
        return DEFAULT_EVAL_PATH
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def load_eval_cases(path: str | Path | None = None) -> list[AgentCourseEvalCase]:
    resolved = resolve_eval_path(path)
    cases: list[AgentCourseEvalCase] = []
    for line_no, line in enumerate(resolved.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        cases.append(AgentCourseEvalCase.from_dict(json.loads(line), line_no))
    return cases


def evaluate_agent_course(answerer: Answerer, cases: Iterable[AgentCourseEvalCase]) -> dict:
    rows = []
    by_route: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "correct": 0})

    for case in cases:
        result = answerer.answer(case.question, session_id=f"eval-{case.id}")
        actual_route = result.route
        route_ok = actual_route == case.expected_route
        by_route[case.expected_route]["total"] += 1
        by_route[case.expected_route]["correct"] += int(route_ok)
        rows.append(
            {
                "id": case.id,
                "question": case.question,
                "expected_route": case.expected_route,
                "actual_route": actual_route,
                "route_ok": route_ok,
                "citation_count": len(result.citations),
                "needs_clarification": result.needs_clarification,
            }
        )

    total = len(rows)
    correct = sum(1 for row in rows if row["route_ok"])
    by_route_report = {
        route: {
            "total": values["total"],
            "correct": values["correct"],
            "accuracy": round(values["correct"] / values["total"], 4)
            if values["total"]
            else 0.0,
        }
        for route, values in sorted(by_route.items())
    }
    return {
        "total": total,
        "correct": correct,
        "route_accuracy": round(correct / total, 4) if total else 0.0,
        "by_route": by_route_report,
        "failures": [row for row in rows if not row["route_ok"]],
        "rows": rows,
    }


run_agent_course_eval = evaluate_agent_course


def _print_report(report: dict) -> None:
    print(f"Total: {report['total']}")
    print(f"Route accuracy: {report['route_accuracy']:.4f}")
    for route, values in report["by_route"].items():
        print(
            f"- {route}: {values['correct']}/{values['total']} "
            f"({values['accuracy']:.4f})"
        )
    if report["failures"]:
        print("\nFailures:")
        for row in report["failures"]:
            print(
                f"- {row['id']}: expected={row['expected_route']} "
                f"actual={row['actual_route']}"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agent course RAG offline evaluation")
    parser.add_argument("--file", default=str(DEFAULT_EVAL_PATH), help="JSONL eval dataset")
    parser.add_argument("--json", action="store_true", help="Print raw JSON report")
    parser.add_argument("--min-route-accuracy", type=float, default=0.8)
    args = parser.parse_args(argv)

    cases = load_eval_cases(args.file)
    from core.agent_course_loader import build_agent_course_orchestrator

    report = evaluate_agent_course(build_agent_course_orchestrator(), cases)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_report(report)
    return 0 if report["route_accuracy"] >= args.min_route_accuracy else 1


if __name__ == "__main__":
    raise SystemExit(main())
