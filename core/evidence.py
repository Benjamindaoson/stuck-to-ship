from dataclasses import dataclass

from core.access_control import access_denial_reason
from core.prompt_injection import has_prompt_injection


@dataclass(frozen=True)
class Evidence:
    text: str
    source_path: str
    score: float
    title: str = ""
    source_type: str = ""
    start_line: int | None = None
    end_line: int | None = None


@dataclass(frozen=True)
class EvidencePacket:
    query: str
    evidence: list[Evidence]
    confidence: float
    blocked_evidence: list[dict]


def build_evidence_packet(query: str, candidates: list[dict], *, user_id: str | None = None) -> EvidencePacket:
    evidence: list[Evidence] = []
    blocked: list[dict] = []
    for item in candidates:
        text = str(item.get("text") or item.get("content") or "").strip()
        if not text:
            continue
        denial = access_denial_reason(item, user_id)
        if denial:
            blocked.append(_blocked(item, denial))
            continue
        if has_prompt_injection(text):
            blocked.append(_blocked(item, "prompt_injection"))
            continue
        evidence.append(
            Evidence(
                text=text,
                source_path=str(item.get("source_path") or item.get("source") or ""),
                score=float(item.get("score") or item.get("rerank_score") or 0.0),
                title=str(item.get("title") or ""),
                source_type=str(item.get("source_type") or ""),
                start_line=item.get("start_line"),
                end_line=item.get("end_line"),
            )
        )
    confidence = max((item.score for item in evidence), default=0.0)
    return EvidencePacket(query=query, evidence=evidence, confidence=confidence, blocked_evidence=blocked)


def _blocked(item: dict, reason: str) -> dict:
    return {
        "reason": reason,
        "source_path": str(item.get("source_path") or item.get("source") or ""),
        "title": str(item.get("title") or ""),
        "source_type": str(item.get("source_type") or ""),
    }
