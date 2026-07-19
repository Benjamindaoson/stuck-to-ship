from pathlib import Path

from core.intent_router import route_query
from core.qa_orchestrator import QAResult
from evaluation.agent_course_eval import evaluate_agent_course, load_eval_cases


DATASET = Path("data/agent_course_eval/manual_v1.jsonl")


class RouterOnlyOrchestrator:
    def answer(self, query, session_id=None):
        route = route_query(query).route
        return QAResult(
            answer="stub",
            route=route,
            citations=[{"source_path": "stub.md", "score": 1.0}]
            if route in {"code", "faq", "error"}
            else [],
            trace={"route": route, "session_id": session_id or ""},
            needs_clarification=route == "clarify",
        )


def test_agent_course_eval_dataset_has_minimum_coverage():
    cases = load_eval_cases(DATASET)

    assert len(cases) >= 30
    assert {"course", "code", "error", "faq", "learning_path", "clarify"} <= {
        case.expected_route for case in cases
    }
    assert all(case.question for case in cases)
    assert all(case.target_behavior for case in cases)


def test_evaluate_agent_course_reports_route_accuracy():
    cases = load_eval_cases(DATASET)

    report = evaluate_agent_course(RouterOnlyOrchestrator(), cases)

    assert report["total"] == len(cases)
    assert report["route_accuracy"] >= 0.95
    assert report["by_route"]["code"]["total"] > 0
    assert report["by_route"]["error"]["total"] > 0


def test_real_agent_course_eval_has_citations_for_answerable_routes():
    from core.agent_course_loader import build_agent_course_orchestrator

    cases = load_eval_cases(DATASET)
    report = evaluate_agent_course(build_agent_course_orchestrator(), cases)

    answerable_routes = {"course", "code", "error", "faq", "learning_path"}
    rows = [row for row in report["rows"] if row["expected_route"] in answerable_routes]

    assert rows
    assert all(row["citation_count"] > 0 for row in rows)
