from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    route: str
    confidence: float
    reason: str
    needs_clarification: bool = False


ERROR_KEYWORDS = (
    "error",
    "exception",
    "traceback",
    "modulenotfounderror",
    "connection refused",
    "unauthorized",
    "报错",
    "失败",
)
CODE_KEYWORDS = (
    "main.py",
    ".py",
    "function",
    "class",
    "api",
    "config",
    "defined",
    "source file",
    "函数",
    "类",
    "启动",
    "接口",
    "配置文件",
)
FAQ_KEYWORDS = (
    "api key",
    "apikey",
    "dashscope",
    "how do i configure",
    "怎么配置",
    "多少钱",
    "课程价格",
)
LEARNING_KEYWORDS = (
    "next step",
    "next steps",
    "learning path",
    "study path",
    "roadmap",
    "what should i learn",
    "learn before",
    "下一步",
    "学习路径",
    "先学",
    "怎么学",
)
AMBIGUOUS_QUERIES = {"这个怎么弄？", "怎么弄", "不会", "help", "?"}


def route_query(query: str) -> RouteDecision:
    q = query.strip()
    lowered = q.lower()
    if lowered in AMBIGUOUS_QUERIES or q in AMBIGUOUS_QUERIES:
        return RouteDecision("clarify", 0.9, "query_too_ambiguous", True)
    if any(item in lowered for item in ERROR_KEYWORDS):
        return RouteDecision("error", 0.86, "matched_error_keywords")
    if any(item in lowered for item in FAQ_KEYWORDS):
        return RouteDecision("faq", 0.8, "matched_faq_keywords")
    if "function calling" in lowered or "tool calling" in lowered:
        return RouteDecision("course", 0.74, "matched_llm_concept_keywords")
    if any(item in lowered for item in CODE_KEYWORDS) or "_" in q:
        return RouteDecision("code", 0.78, "matched_code_keywords")
    if any(item in lowered for item in LEARNING_KEYWORDS):
        return RouteDecision("learning_path", 0.76, "matched_learning_keywords")
    return RouteDecision("course", 0.65, "default_course_route")
