from types import SimpleNamespace

from fastapi.testclient import TestClient


class StubRagService:
    def resolve_session_id(self, session_id=None, user_id=None):
        return session_id or user_id or "s1"

    async def ask(self, **kwargs):
        return {
            "answer": "ok",
            "references": [],
            "latency_ms": 1,
            "complexity": "course",
            "route": "course",
            "trace": {},
            "record_id": None,
            "session_id": kwargs.get("session_id") or "s1",
        }


def _app_with_stub():
    from main import AppState, create_app

    return create_app(
        app_state=AppState(
            vector_store=SimpleNamespace(collection_stats={}),
            rag_graph=None,
            rag_service=StubRagService(),
            document_service=SimpleNamespace(),
            knowledge_service=SimpleNamespace(),
            analytics_service=SimpleNamespace(),
        ),
        initialize_runtime=False,
    )


def test_api_key_auth_blocks_api_when_keys_are_configured(monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "API_KEYS", {"secret"})
    client = TestClient(_app_with_stub())

    response = client.post("/api/v1/rag/ask", json={"query": "What is RAG?"})

    assert response.status_code == 401


def test_api_key_auth_accepts_bearer_or_x_api_key(monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "API_KEYS", {"secret"})
    client = TestClient(_app_with_stub())

    bearer = client.post(
        "/api/v1/rag/ask",
        json={"query": "What is RAG?", "session_id": "s1"},
        headers={"Authorization": "Bearer secret"},
    )
    header = client.post(
        "/api/v1/rag/ask",
        json={"query": "What is RAG?", "session_id": "s1"},
        headers={"X-API-Key": "secret"},
    )

    assert bearer.status_code == 200
    assert header.status_code == 200
