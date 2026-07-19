from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = {"", "ollama", "change-me", "replace-me"}
REQUIRED = {
    "LLM_API_KEY": "real model API key",
    "LLM_BASE_URL": "OpenAI-compatible base URL",
    "LLM_MODEL": "model name",
    "STUCKTOSHIP_API_KEYS": "API key protecting /api routes",
    "STUCKTOSHIP_MILVUS_URI": "Milvus or Zilliz endpoint",
}
ALIASES = {"LLM_API_KEY": ("DEEPSEEK_API_KEY",)}


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _value(env: dict[str, str], key: str) -> str:
    value = env.get(key) or os.getenv(key, "")
    if value:
        return value
    for alias in ALIASES.get(key, ()):
        value = env.get(alias) or os.getenv(alias, "")
        if value:
            return value
    return ""


def _is_placeholder(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered in PLACEHOLDERS or "replace-with" in lowered


def _root_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / value.strip("./\\")


def check(env_file: Path | None = None) -> tuple[list[str], list[str]]:
    env = _load_env_file(env_file) if env_file else {}
    errors: list[str] = []
    warnings: list[str] = []

    for key, description in REQUIRED.items():
        value = _value(env, key)
        if _is_placeholder(value):
            aliases = ", ".join(ALIASES.get(key, ()))
            suffix = f"; aliases: {aliases}" if aliases else ""
            errors.append(f"{key} is missing or placeholder ({description}{suffix})")

    milvus_uri = _value(env, "STUCKTOSHIP_MILVUS_URI")
    if milvus_uri and not milvus_uri.startswith(("http://", "https://")):
        warnings.append("STUCKTOSHIP_MILVUS_URI is not an HTTP endpoint; use Milvus/Zilliz for production")

    knowledge_dir = _root_path(_value(env, "KNOWLEDGE_DIR") or "./knowledge")
    if not knowledge_dir.exists():
        errors.append(f"KNOWLEDGE_DIR does not exist: {knowledge_dir}")
    elif not any((knowledge_dir / name).exists() for name in ("courses", "faq", "errors")):
        warnings.append("KNOWLEDGE_DIR has no courses/, faq/, or errors/ directories")

    eval_dataset = _root_path(_value(env, "EVAL_DATASET") or "./data/agent_course_eval/manual_v1.jsonl")
    if not eval_dataset.exists():
        warnings.append(f"EVAL_DATASET does not exist: {eval_dataset}")

    for file_name in ("Dockerfile", "docker-compose.production.yml"):
        if not (ROOT / file_name).exists():
            errors.append(f"{file_name} is missing")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check StuckToShip production configuration.")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env.production")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors, warnings = check(args.env_file)
    payload = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("OK" if payload["ok"] else "NOT READY")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN: {item}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
