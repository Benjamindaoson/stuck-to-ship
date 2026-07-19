def test_extract_python_symbols(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        "import os\n\nclass Runner:\n    def start(self):\n        return os.getcwd()\n",
        encoding="utf-8",
    )

    from ingestion.code_indexer import extract_python_symbols

    symbols = extract_python_symbols(tmp_path)
    names = {item.symbol_name for item in symbols}
    assert "Runner" in names
    assert "start" in names


def test_search_code_symbols_matches_function_name(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("def build_rag_graph():\n    return None\n", encoding="utf-8")

    from ingestion.code_indexer import extract_python_symbols
    from core.code_retriever import search_code_symbols

    symbols = extract_python_symbols(tmp_path)
    results = search_code_symbols("build_rag_graph 在哪里？", symbols)
    assert results[0]["symbol_name"] == "build_rag_graph"
    assert results[0]["source_path"].endswith("sample.py")
    assert results[0]["start_line"] == 1
