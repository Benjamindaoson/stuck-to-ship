from __future__ import annotations

import re


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]{2,}")
LEARNING_TERMS = ("learning path", "study", "roadmap", "next", "学习路径", "下一步", "先学")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "before",
    "does",
    "for",
    "how",
    "in",
    "is",
    "it",
    "of",
    "or",
    "should",
    "the",
    "to",
    "what",
    "when",
    "where",
    "why",
}


def search_course_docs(
    query: str,
    docs: list[dict],
    *,
    route: str = "course",
    limit: int = 5,
) -> list[dict]:
    query_tokens = _tokens(query)
    scored: list[tuple[float, dict]] = []

    for doc in docs:
        text = str(doc.get("text") or "")
        haystack = f"{doc.get('title', '')} {text} {' '.join(doc.get('tags') or [])}".lower()
        score = _overlap_score(query_tokens, haystack)
        if route == "learning_path" and any(term in haystack for term in LEARNING_TERMS):
            score = max(score, 0.72)
        if score:
            scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            **doc,
            "text": doc.get("text", ""),
            "score": round(score, 4),
            "source_path": str(doc.get("source_path") or doc.get("source") or ""),
            "source_type": str(doc.get("source_type") or "course_note"),
        }
        for score, doc in scored[:limit]
    ]


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in (match.group(0).lower() for match in TOKEN_RE.finditer(text))
        if token not in STOPWORDS
    ]


def _overlap_score(query_tokens: list[str], haystack: str) -> float:
    if not query_tokens:
        return 0.0
    hits = sum(1 for token in query_tokens if token in haystack)
    if not hits:
        return 0.0
    return min(1.0, 0.35 + hits / len(query_tokens))
