from dataclasses import dataclass

from core.evidence import EvidencePacket


@dataclass(frozen=True)
class GateDecision:
    action: str
    reason: str


def decide_evidence(packet: EvidencePacket, min_score: float = 0.45) -> GateDecision:
    if not packet.evidence:
        if packet.blocked_evidence:
            return GateDecision("clarify_or_refuse", packet.blocked_evidence[0]["reason"])
        return GateDecision("clarify_or_refuse", "no_evidence")
    if packet.confidence < min_score:
        return GateDecision("retry", "low_confidence")
    if not any(item.source_path for item in packet.evidence):
        return GateDecision("clarify_or_refuse", "missing_source")
    return GateDecision("accept", "evidence_supported")
