"""Shared state definitions for the RAG workflow."""

from typing import Any, TypedDict


MAX_ROUNDS = 10


class RAGState(TypedDict):
    """RAG 流程的全局状态"""

    query: str
    subject: str | None
    grade: str | None
    session_id: str
    route: str
    trace: dict[str, Any]
    intent: str
    complexity: str
    retrieved_docs: list
    answer: str
    retry_count: int
    max_retries: int
    conversation_history: list[dict]
    retrieval_plan: dict
    retrieval_attempts: list[dict]
    retrieval_metrics: dict
    retrieval_decision: dict
    normalized_evidence: list[dict]
    selected_tools: list[str]
    planner_budget: dict[str, int]
    gate_decision: dict[str, Any]
    citations: list[dict]
    redacted_trace: dict[str, Any]
    fast_path_result: bool
    abstain_reason: str
    retrieval_latency_ms: float
    rerank_latency_ms: float
    reranker_available: bool
    sub_queries: list[str]
    _queue_id: str
