from __future__ import annotations

from collections.abc import Iterable


def access_denial_reason(candidate: dict, user_id: str | None) -> str | None:
    allowed = _allowed_users(candidate)
    visibility = str(candidate.get("visibility") or "public").lower()
    if visibility not in {"private", "restricted"} and not allowed:
        return None
    if user_id and user_id in allowed:
        return None
    return "acl_denied"


def _allowed_users(candidate: dict) -> set[str]:
    raw = candidate.get("allowed_users") or candidate.get("allowed_user_ids") or []
    if isinstance(raw, str):
        return {item.strip() for item in raw.split(",") if item.strip()}
    if isinstance(raw, Iterable):
        return {str(item).strip() for item in raw if str(item).strip()}
    return set()
