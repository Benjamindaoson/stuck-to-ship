from pathlib import Path


def test_milvus_compose_exposes_standalone_endpoint():
    compose = Path("docker-compose.milvus.yml").read_text(encoding="utf-8")

    assert "milvus-standalone" in compose
    assert "19530:19530" in compose
    assert "etcd" in compose
    assert "minio" in compose
