from __future__ import annotations

import argparse
import os
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_env() -> str:
    api_key = secrets.token_urlsafe(32)
    llm_key_note = (
        "# DEEPSEEK_API_KEY is already set in the parent environment.\n"
        "# Keep the value out of this file.\n"
        if os.getenv("DEEPSEEK_API_KEY")
        else "# Set DEEPSEEK_API_KEY in the server environment, or uncomment LLM_API_KEY below.\n"
    )
    return "\n".join(
        [
            "APP_MODE=agent_course",
            "APP_HOST=0.0.0.0",
            "APP_PORT=8000",
            "LOG_LEVEL=INFO",
            "",
            "ENABLE_TRACE=true",
            "ENABLE_FAQ_FIRST=true",
            "ENABLE_EVALUATION_API=false",
            "",
            "KNOWLEDGE_DIR=./knowledge",
            "CODE_RAG_ROOTS=.",
            "EVAL_DATASET=./data/agent_course_eval/manual_v1.jsonl",
            "",
            llm_key_note.rstrip(),
            "# LLM_API_KEY=replace-with-real-llm-key",
            "LLM_BASE_URL=https://api.deepseek.com",
            "LLM_MODEL=deepseek-v4-flash",
            f"STUCKTOSHIP_API_KEYS={api_key}",
            "STUCKTOSHIP_MILVUS_URI=http://milvus-standalone:19530",
            "",
            "EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5",
            "EMBEDDING_DEVICE=cpu",
            "ENABLE_RERANKER=true",
            "RERANKER_MODEL=BAAI/bge-reranker-base",
            "RERANKER_DEVICE=cpu",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a local .env.production file.")
    parser.add_argument("--output", type=Path, default=ROOT / ".env.production")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists() and not args.force:
        print(f"exists: {output}")
        return 0
    output.write_text(build_env(), encoding="utf-8")
    print(f"created: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
