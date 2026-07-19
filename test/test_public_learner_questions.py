import json
from pathlib import Path


DATASET = Path("data/learner_questions/public_ai_engineering_questions.jsonl")


def test_public_learner_question_seed_count_and_schema():
    rows = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert 50 <= len(rows) <= 100
    assert len({row["id"] for row in rows}) == len(rows)

    for row in rows:
        assert row["question"].strip().endswith("？")
        assert row["source_url"].startswith(("https://github.com/", "https://stackoverflow.com/"))
        assert row["license_note"] == "public_source_paraphrased"
