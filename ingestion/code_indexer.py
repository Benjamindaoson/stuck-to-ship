from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CodeSymbol:
    source_path: str
    symbol_name: str
    symbol_type: str
    start_line: int
    end_line: int
    text: str
    imports: tuple[str, ...] = ()


def extract_python_symbols(root: Path) -> list[CodeSymbol]:
    results: list[CodeSymbol] = []
    for path in Path(root).rglob("*.py"):
        if any(part in {".venv", "__pycache__", ".git"} for part in path.parts):
            continue
        source = path.read_text(encoding="utf-8", errors="ignore")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        lines = source.splitlines()
        imports = tuple(_module_imports(tree))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = getattr(node, "lineno", 1)
                end = getattr(node, "end_lineno", start)
                results.append(
                    CodeSymbol(
                        source_path=str(path),
                        symbol_name=node.name,
                        symbol_type="class" if isinstance(node, ast.ClassDef) else "function",
                        start_line=start,
                        end_line=end,
                        text="\n".join(lines[start - 1 : end]),
                        imports=imports,
                    )
                )
    return results


def _module_imports(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports
