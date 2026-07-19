from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import replace
from typing import Awaitable

from core.access_control import access_denial_reason
from core.evidence import Evidence, EvidencePacket
from core.prompt_injection import has_prompt_injection
from core.retrieval.contracts import EvidenceCandidate, EvidenceSet, RetrievalPlan, RetrievalQuery, Retriever
from core.retrieval_gate import decide_evidence


Reranker = Callable[
    [RetrievalQuery, list[EvidenceCandidate]],
    list[EvidenceCandidate] | Awaitable[list[EvidenceCandidate]],
]


class UnifiedRetrievalEngine:
    def __init__(self, retrievers: dict[str, Retriever], reranker: Reranker | None = None):
        self.retrievers = retrievers
        self.reranker = reranker

    async def retrieve(self, plan: RetrievalPlan) -> EvidenceSet:
        candidates: list[EvidenceCandidate] = []
        blocked: list[dict] = []
        for tool in plan.tools:
            retriever = self.retrievers.get(tool)
            if retriever is None:
                blocked.append({"reason": "unregistered_tool", "tool": tool})
                continue
            candidates.extend(await retriever.retrieve(plan.query))

        allowed, blocked_evidence = _filter_candidates(candidates, plan.query.user_id)
        blocked.extend(blocked_evidence)
        fused = fuse_candidates(allowed)[: plan.top_k]
        if self.reranker is not None:
            reranked = self.reranker(plan.query, fused)
            fused = await reranked if inspect.isawaitable(reranked) else reranked
        decision = _gate(plan.query, fused, blocked)
        return EvidenceSet(evidence=fused, blocked_evidence=blocked, decision=decision)


def fuse_candidates(candidates: list[EvidenceCandidate]) -> list[EvidenceCandidate]:
    by_id: dict[str, EvidenceCandidate] = {}
    strategies: dict[str, list[str]] = {}
    for candidate in candidates:
        existing = by_id.get(candidate.id)
        if existing is None:
            by_id[candidate.id] = candidate
            strategies[candidate.id] = [candidate.retrieval_strategy]
            continue

        raw_scores = {**existing.raw_scores, **candidate.raw_scores}
        metadata = {**existing.metadata, **candidate.metadata}
        if candidate.retrieval_strategy not in strategies[candidate.id]:
            strategies[candidate.id].append(candidate.retrieval_strategy)
        by_id[candidate.id] = replace(
            existing,
            raw_scores=raw_scores,
            retrieval_strategy="+".join(strategies[candidate.id]),
            metadata=metadata,
        )

    return sorted(by_id.values(), key=lambda item: (-_best_score(item), item.id))


def _best_score(candidate: EvidenceCandidate) -> float:
    return max(candidate.raw_scores.values(), default=0.0)


def _filter_candidates(
    candidates: list[EvidenceCandidate],
    user_id: str | None,
) -> tuple[list[EvidenceCandidate], list[dict]]:
    allowed: list[EvidenceCandidate] = []
    blocked: list[dict] = []
    for candidate in candidates:
        if not candidate.id or not candidate.source_path:
            blocked.append(_blocked(candidate, "missing_source"))
            continue
        denial = access_denial_reason({**candidate.metadata, "source_path": candidate.source_path}, user_id)
        if denial:
            blocked.append(_blocked(candidate, denial))
            continue
        if has_prompt_injection(candidate.text):
            blocked.append(_blocked(candidate, "prompt_injection"))
            continue
        allowed.append(candidate)
    return allowed, blocked


def _blocked(candidate: EvidenceCandidate, reason: str) -> dict:
    return {"reason": reason, "id": candidate.id, "source_path": candidate.source_path}


def _gate(query: RetrievalQuery, candidates: list[EvidenceCandidate], blocked: list[dict]) -> dict[str, object]:
    packet = EvidencePacket(
        query=query.text,
        evidence=[
            Evidence(
                text=item.text,
                source_path=item.source_path,
                source_type=item.source_type,
                score=_best_score(item),
                title=str(item.metadata.get("title") or ""),
                start_line=_int_or_none(item.location.get("start_line")),
                end_line=_int_or_none(item.location.get("end_line")),
            )
            for item in candidates
        ],
        confidence=max((_best_score(item) for item in candidates), default=0.0),
        blocked_evidence=blocked,
    )
    decision = decide_evidence(packet)
    return {"action": decision.action, "reason": decision.reason}


def _int_or_none(value: object) -> int | None:
    return value if isinstance(value, int) else None
