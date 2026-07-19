import pytest


@pytest.mark.parametrize(
    ("query", "route"),
    [
        ("RAG 和微调有什么区别？", "course"),
        ("ModuleNotFoundError: No module named 'pymilvus'", "error"),
        ("main.py 是从哪里启动 FastAPI 的？", "code"),
        ("DashScope API Key 怎么配置？", "faq"),
        ("我下一步应该学 LangGraph 还是 MCP？", "learning_path"),
    ],
)
def test_route_query(query, route):
    from core.intent_router import route_query

    decision = route_query(query)
    assert decision.route == route
    assert decision.confidence > 0


def test_unclear_query_requests_clarification():
    from core.intent_router import route_query

    decision = route_query("这个怎么弄？")
    assert decision.route == "clarify"
    assert decision.needs_clarification is True
