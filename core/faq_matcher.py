from difflib import SequenceMatcher


def match_faq(query: str, faqs: list[dict], threshold: float = 0.86) -> dict | None:
    q = query.strip().lower()
    best_score = 0.0
    best: dict | None = None
    for item in faqs:
        question = str(item.get("question", "")).strip().lower()
        if not question:
            continue
        score = 1.0 if question in q or q in question else SequenceMatcher(None, q, question).ratio()
        if score > best_score:
            best_score = score
            best = item
    if best is None or best_score < threshold:
        return None
    return {
        **best,
        "score": best_score,
        "source_type": "faq",
        "source_path": str(best.get("source_path") or best.get("source") or "faq"),
    }
