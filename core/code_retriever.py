from ingestion.code_indexer import CodeSymbol


def search_code_symbols(query: str, symbols: list[CodeSymbol], limit: int = 5) -> list[dict]:
    q = query.lower()
    tokens = [token for token in q.replace("?", " ").replace("？", " ").split() if token]
    scored: list[tuple[float, CodeSymbol]] = []
    for symbol in symbols:
        haystack = f"{symbol.symbol_name} {symbol.source_path} {symbol.text}".lower()
        score = 0.0
        if symbol.symbol_name.lower() in q:
            score += 2.0
        if any(token in haystack for token in tokens):
            score += 0.5
        if score:
            scored.append((score, symbol))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "text": symbol.text,
            "source_path": symbol.source_path,
            "symbol_name": symbol.symbol_name,
            "symbol_type": symbol.symbol_type,
            "start_line": symbol.start_line,
            "end_line": symbol.end_line,
            "score": score,
            "source_type": "project_code",
        }
        for score, symbol in scored[:limit]
    ]
