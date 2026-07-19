def test_agent_course_settings_exist():
    from config import settings

    assert settings.APP_MODE == "agent_course"
    assert settings.ENABLE_TRACE is True
    assert settings.ENABLE_FAQ_FIRST is True
    assert settings.ENABLE_EVALUATION_API is True
    assert settings.FAQ_DIRECT_THRESHOLD == 0.86
    assert settings.RETRIEVAL_MIN_SCORE == 0.45
    assert settings.KNOWLEDGE_DIR.endswith("knowledge")
    assert settings.EVAL_DATASET.endswith("manual_v1.jsonl")


def test_stucktoship_milvus_uri_is_primary():
    import os
    import subprocess
    import sys

    env = os.environ.copy()
    env["STUCKTOSHIP_MILVUS_URI"] = "http://milvus:19530"

    result = subprocess.run(
        [sys.executable, "-c", "import config; print(config.settings.MILVUS_URI)"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )

    assert result.stdout.strip() == "http://milvus:19530"


def test_stucktoship_api_keys_are_comma_separated():
    import os
    import subprocess
    import sys

    env = os.environ.copy()
    env["STUCKTOSHIP_API_KEYS"] = "one, two ,,three"

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import config; print(','.join(sorted(config.settings.API_KEYS)))",
        ],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )

    assert result.stdout.strip() == "one,three,two"


def test_deepseek_api_key_is_llm_api_key_fallback():
    import os
    import subprocess
    import sys

    env = os.environ.copy()
    env.pop("LLM_API_KEY", None)
    env["DEEPSEEK_API_KEY"] = "deepseek-test-key"

    result = subprocess.run(
        [sys.executable, "-c", "import config; print(config.settings.LLM_API_KEY)"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )

    assert result.stdout.strip() == "deepseek-test-key"
