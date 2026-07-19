from __future__ import annotations

import json
import os
import re
from pathlib import Path

from config import BASE_DIR, settings
from core.qa_orchestrator import QAOrchestrator
from ingestion.code_indexer import CodeSymbol, extract_python_symbols
from utils.logger import logger


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return Path(BASE_DIR) / candidate


def load_jsonl_records(path: str | Path) -> list[dict]:
    resolved = resolve_project_path(path)
    if not resolved.exists():
        return []

    files = [resolved] if resolved.is_file() else sorted(resolved.rglob("*.jsonl"))
    records: list[dict] = []
    for file_path in files:
        for line_no, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{file_path}:{line_no}: invalid JSONL record") from exc
            if isinstance(item, dict):
                item.setdefault("source_path", str(file_path))
                records.append(item)
    return records


def load_faqs(knowledge_dir: str | Path) -> list[dict]:
    return load_jsonl_records(resolve_project_path(knowledge_dir) / "faq")


def load_error_recipes(knowledge_dir: str | Path) -> list[dict]:
    return load_jsonl_records(resolve_project_path(knowledge_dir) / "errors")


def load_course_docs(knowledge_dir: str | Path) -> list[dict]:
    courses_dir = resolve_project_path(knowledge_dir) / "courses"
    if not courses_dir.exists():
        return []

    docs: list[dict] = []
    for path in sorted(courses_dir.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        raw_lines = path.read_text(encoding="utf-8").splitlines()
        metadata, lines = _split_front_matter(raw_lines)
        title = _title_from_lines(lines, path.stem)
        source_type = metadata.get(
            "source_type",
            "course_outline" if "path" in path.stem or "outline" in path.stem else "course_note",
        )
        docs.append(
            {
                **metadata,
                "title": title,
                "text": "\n".join(lines).strip(),
                "source_path": str(path),
                "source_type": source_type,
                "start_line": 1,
                "end_line": len(lines),
            }
        )
    return docs


def parse_code_roots(raw_roots: str | Path) -> list[Path]:
    raw = str(raw_roots).replace(",", os.pathsep)
    roots = []
    for item in raw.split(os.pathsep):
        if not item.strip():
            continue
        root = resolve_project_path(item.strip())
        if root.exists():
            roots.append(root)
    return roots


def load_code_symbols(code_roots: str | Path) -> list[CodeSymbol]:
    symbols: list[CodeSymbol] = []
    for root in parse_code_roots(code_roots):
        symbols.extend(extract_python_symbols(root))
    return symbols


def build_agent_course_orchestrator(
    *,
    knowledge_dir: str | Path | None = None,
    code_roots: str | Path | None = None,
) -> QAOrchestrator:
    knowledge_root = knowledge_dir or settings.KNOWLEDGE_DIR
    code_root_values = code_roots or settings.CODE_RAG_ROOTS
    faqs = load_faqs(knowledge_root)
    error_recipes = load_error_recipes(knowledge_root)
    course_docs = load_course_docs(knowledge_root)
    code_symbols = load_code_symbols(code_root_values)

    logger.info(
        "Agent course data loaded: faqs=%d, error_recipes=%d, course_docs=%d, code_symbols=%d",
        len(faqs),
        len(error_recipes),
        len(course_docs),
        len(code_symbols),
    )
    return QAOrchestrator(
        code_symbols=code_symbols,
        course_docs=course_docs,
        faqs=faqs,
        error_recipes=error_recipes,
    )


def _title_from_lines(lines: list[str], fallback: str) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _split_front_matter(lines: list[str]) -> tuple[dict, list[str]]:
    if not lines or lines[0].strip() != "---":
        return {}, lines
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, lines

    metadata: dict[str, object] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = _parse_front_matter_value(value.strip())
    return metadata, lines[end + 1 :]


def _parse_front_matter_value(value: str):
    if value.startswith("[") and value.endswith("]"):
        return [
            item.strip().strip("'\"")
            for item in value[1:-1].split(",")
            if item.strip()
        ]
    if re.fullmatch(r"true|false", value, re.IGNORECASE):
        return value.lower() == "true"
    return value.strip("'\"")
