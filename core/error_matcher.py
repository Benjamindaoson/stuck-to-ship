def match_error_recipe(query: str, recipes: list[dict]) -> dict | None:
    q = query.lower()
    for item in recipes:
        pattern = str(item.get("error_pattern", "")).lower()
        if pattern and pattern in q:
            return {
                **item,
                "score": 1.0,
                "source_type": "error_recipe",
                "source_path": str(item.get("source_path") or item.get("source") or "errors"),
            }
    return None
