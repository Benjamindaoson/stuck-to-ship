import json
import os
import subprocess
import sys
from pathlib import Path


def test_production_env_example_and_readiness_check_exist():
    assert Path(".env.production.example").exists()
    assert Path("scripts/check_production_ready.py").exists()
    assert Path("scripts/bootstrap_production_env.py").exists()
    assert Path("docs/production-readiness.md").exists()


def test_production_readiness_check_fails_on_placeholders(tmp_path):
    env_file = tmp_path / ".env.production"
    env_file.write_text(
        "\n".join(
            [
                "LLM_API_KEY=replace-with-real-llm-key",
                "LLM_BASE_URL=https://api.deepseek.com",
                "LLM_MODEL=deepseek-v4-flash",
                "STUCKTOSHIP_API_KEYS=replace-with-long-random-api-key",
                "STUCKTOSHIP_MILVUS_URI=http://milvus.example.test:19530",
                "KNOWLEDGE_DIR=./knowledge",
                "EVAL_DATASET=./data/agent_course_eval/manual_v1.jsonl",
            ]
        ),
        encoding="utf-8",
    )

    env = os.environ.copy()
    env.pop("LLM_API_KEY", None)
    env.pop("DEEPSEEK_API_KEY", None)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_production_ready.py",
            "--env-file",
            str(env_file),
            "--json",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["ok"] is False
    assert any("LLM_API_KEY" in error for error in payload["errors"])


def test_production_readiness_check_accepts_minimal_real_values(tmp_path):
    env_file = tmp_path / ".env.production"
    env_file.write_text(
        "\n".join(
            [
                "LLM_API_KEY=test-real-key",
                "LLM_BASE_URL=https://api.example.test/v1",
                "LLM_MODEL=test-model",
                "STUCKTOSHIP_API_KEYS=test-api-key",
                "STUCKTOSHIP_MILVUS_URI=http://milvus.example.test:19530",
                "KNOWLEDGE_DIR=./knowledge",
                "EVAL_DATASET=./data/agent_course_eval/manual_v1.jsonl",
            ]
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_production_ready.py",
            "--env-file",
            str(env_file),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["ok"] is True


def test_production_readiness_check_accepts_deepseek_alias(tmp_path):
    env_file = tmp_path / ".env.production"
    env_file.write_text(
        "\n".join(
            [
                "DEEPSEEK_API_KEY=test-deepseek-key",
                "LLM_BASE_URL=https://api.deepseek.com",
                "LLM_MODEL=deepseek-v4-flash",
                "STUCKTOSHIP_API_KEYS=test-api-key",
                "STUCKTOSHIP_MILVUS_URI=http://milvus.example.test:19530",
                "KNOWLEDGE_DIR=./knowledge",
                "EVAL_DATASET=./data/agent_course_eval/manual_v1.jsonl",
            ]
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_production_ready.py",
            "--env-file",
            str(env_file),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["ok"] is True


def test_bootstrap_production_env_generates_local_api_key(tmp_path):
    env_file = tmp_path / ".env.production"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/bootstrap_production_env.py",
            "--output",
            str(env_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    content = env_file.read_text(encoding="utf-8")

    assert "created:" in result.stdout
    assert "STUCKTOSHIP_API_KEYS=" in content
    assert "replace-with-long-random-api-key" not in content
    assert "DEEPSEEK_API_KEY=" not in content
