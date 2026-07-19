from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class RetrievalQuery:
    text: str
    route: str
    user_id: str | None = None
    filters: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceCandidate:
    id: str
    text: str
    source_path: str
    source_type: str
    modality: str
    location: dict[str, int | float | str] = field(default_factory=dict)
    raw_scores: dict[str, float] = field(default_factory=dict)
    retrieval_strategy: str = ""
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalPlan:
    query: RetrievalQuery
    tools: tuple[str, ...]
    top_k: int = 10


@dataclass(frozen=True)
class EvidenceSet:
    evidence: list[EvidenceCandidate]
    blocked_evidence: list[dict]
    decision: dict[str, object]


@runtime_checkable
class Retriever(Protocol):
    async def retrieve(self, query: RetrievalQuery) -> list[EvidenceCandidate]:
        ...
