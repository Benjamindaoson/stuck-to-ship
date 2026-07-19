"""Fast keyword intent matcher for the legacy LangGraph pipeline."""

from __future__ import annotations

import time


KEYWORD_INTENT_MAP: list[tuple[str, list[str]]] = [
    (
        "greeting",
        ["你好", "您好", "hi", "hello", "hey", "在吗", "再见", "bye"],
    ),
    (
        "command",
        ["/help", "/exit", "/start", "/model", "帮助", "命令"],
    ),
    (
        "educational",
        [
            "rag",
            "agent",
            "llm",
            "大模型",
            "智能体",
            "向量数据库",
            "embedding",
            "rerank",
            "langgraph",
            "langchain",
            "mcp",
            "function calling",
            "tool calling",
            "prompt",
            "检索",
            "重排",
            "分块",
            "chunk",
            "课程",
            "讲义",
            "项目",
            "源码",
            "代码",
            "架构",
            "启动流程",
            "学习路径",
            "怎么学",
            "什么是",
            "区别",
            "原理",
            "为什么",
            "如何实现",
        ],
    ),
    (
        "technical",
        [
            "bug",
            "报错",
            "异常",
            "traceback",
            "modulenotfounderror",
            "importerror",
            "安装失败",
            "启动失败",
            "连接失败",
            "api key",
            "环境变量",
            "依赖",
            "docker",
            "milvus",
            "uvicorn",
            "fastapi",
        ],
    ),
    (
        "chitchat",
        ["谢谢", "感谢", "thank", "好的", "ok", "测试", "test", "你是谁", "你能做什么"],
    ),
]


def match_keywords(query: str) -> dict | None:
    """Return a fast intent hit, or None when no keyword matches."""
    start = time.perf_counter()
    query_lower = query.strip().lower()

    for intent, keywords in KEYWORD_INTENT_MAP:
        for keyword in keywords:
            if keyword in query_lower:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return {
                    "intent": intent,
                    "confidence": 1.0,
                    "source": "keyword",
                    "processing_time_ms": round(elapsed_ms, 2),
                }

    return None
