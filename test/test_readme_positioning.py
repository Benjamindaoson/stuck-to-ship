from pathlib import Path


def test_readme_stays_ai_engineering_focused():
    text = Path("README.md").read_text(encoding="utf-8")

    assert ("K" + "12") not in text
    assert ("k" + "12") not in text
    assert "StuckToShip" in text
    assert "get unstuck and build the project" in text
    assert "README.zh-CN.md" in text


def test_chinese_readme_stays_ai_engineering_focused():
    text = Path("README.zh-CN.md").read_text(encoding="utf-8")

    assert ("K" + "12") not in text
    assert ("k" + "12") not in text
    assert "从卡住到做出来的 AI 工程课程助教" in text
    assert "可信、有出处是底线；真正的价值是帮学习者打通卡点" in text
    assert "README.md" in text


def test_public_env_uses_stucktoship_milvus_name():
    text = Path(".env.example").read_text(encoding="utf-8")

    assert "STUCKTOSHIP_MILVUS_URI" in text
    assert "STUCKTOSHIP_API_KEYS" in text
    assert ("EDU" + "RAG_MILVUS_URI") not in text
    assert ("K" + "12_MILVUS_URI") not in text
