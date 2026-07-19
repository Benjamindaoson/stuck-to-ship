from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


COURSE_SUFFIXES = {".md", ".txt"}
FAQ_REQUIRED = {"question", "answer"}
ERROR_REQUIRED = {"error_pattern", "symptom", "cause", "fix_steps"}
EVAL_REQUIRED = {"question", "expected_route", "should_answer"}


def import_course_assets(source_dir: str | Path, project_root: str | Path, *, overwrite: bool = False) -> dict[str, Any]:
    source = Path(source_dir).resolve()
    root = Path(project_root).resolve()
    if not source.exists():
        raise FileNotFoundError(f"course data source does not exist: {source}")

    plan = _build_import_plan(source, root)
    _validate_plan(plan)
    _copy_plan(plan, overwrite=overwrite)

    report = {
        "source": str(source),
        "imported_at": datetime.now(UTC).isoformat(),
        "courses": len(plan["courses"]),
        "faq": _count_jsonl_rows(plan["faq"]),
        "errors": _count_jsonl_rows(plan["errors"]),
        "eval": _count_jsonl_rows(plan["eval"]),
        "files": [str(target.relative_to(root)) for _, target in _all_file_pairs(plan)],
    }
    manifest = root / "knowledge" / "course_manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def _build_import_plan(source: Path, root: Path) -> dict[str, list[tuple[Path, Path]]]:
    courses_source = source / "courses"
    if not courses_source.exists():
        courses_source = source

    return {
        "courses": [
            (path, root / "knowledge" / "courses" / path.relative_to(courses_source))
            for path in sorted(courses_source.rglob("*"))
            if path.is_file() and path.suffix.lower() in COURSE_SUFFIXES
        ],
        "faq": _jsonl_pairs(source / "faq", root / "knowledge" / "faq"),
        "errors": _jsonl_pairs(source / "errors", root / "knowledge" / "errors"),
        "eval": _jsonl_pairs(source / "eval", root / "data" / "agent_course_eval"),
    }


def _jsonl_pairs(source_dir: Path, target_dir: Path) -> list[tuple[Path, Path]]:
    if not source_dir.exists():
        return []
    return [
        (path, target_dir / path.relative_to(source_dir))
        for path in sorted(source_dir.rglob("*.jsonl"))
        if path.is_file()
    ]


def _validate_plan(plan: dict[str, list[tuple[Path, Path]]]) -> None:
    for path, _ in plan["faq"]:
        _validate_jsonl(path, FAQ_REQUIRED, "faq")
    for path, _ in plan["errors"]:
        _validate_jsonl(path, ERROR_REQUIRED, "errors")
    for path, _ in plan["eval"]:
        _validate_jsonl(path, EVAL_REQUIRED, "eval")


def _validate_jsonl(path: Path, required: set[str], label: str) -> None:
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{label} {path}:{line_no} invalid JSON") from exc
        missing = sorted(required - set(row))
        if missing:
            raise ValueError(f"{label} {path}:{line_no} missing fields: {', '.join(missing)}")


def _copy_plan(plan: dict[str, list[tuple[Path, Path]]], *, overwrite: bool) -> None:
    for source, target in _all_file_pairs(plan):
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _all_file_pairs(plan: dict[str, list[tuple[Path, Path]]]) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for key in ("courses", "faq", "errors", "eval"):
        pairs.extend(plan[key])
    return pairs


def _count_jsonl_rows(pairs: list[tuple[Path, Path]]) -> int:
    total = 0
    for source, _ in pairs:
        total += sum(1 for line in source.read_text(encoding="utf-8").splitlines() if line.strip())
    return total
