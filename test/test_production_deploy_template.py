from pathlib import Path


def test_production_deploy_template_exists():
    compose = Path("docker-compose.production.yml").read_text(encoding="utf-8")
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")

    assert "stucktoship-api" in compose
    assert "STUCKTOSHIP_MILVUS_URI" in compose
    assert "19530" in compose
    assert "python:3.12" in dockerfile
