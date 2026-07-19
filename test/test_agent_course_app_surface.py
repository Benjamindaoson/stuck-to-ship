def test_agent_course_app_surface_hides_unfinished_routes():
    from main import create_app

    app = create_app(initialize_runtime=False)
    paths = {route.path for route in app.routes}

    assert "/api/v1/rag/ask" in paths
    assert "/api/v1/documents/upload" in paths
    assert "/api/v1/evaluation/history" in paths
    assert not any(path.startswith("/api/v1/analytics") for path in paths)
    assert not any(path.startswith("/api/v1/knowledge-points") for path in paths)


def test_main_exposes_agent_course_orchestrator_initializer():
    import main

    assert callable(main.init_agent_course_orchestrator_sync)


def test_agent_course_runtime_degrades_when_local_milvus_lite_is_unavailable(monkeypatch):
    import sys
    import types

    import main
    from config import settings

    fake_module = types.ModuleType("core.vectorestore")

    class FailingVectorStore:
        def __init__(self):
            raise RuntimeError("milvus-lite is required for local database connections")

    fake_module.StuckToShipVectorStore = FailingVectorStore
    monkeypatch.setitem(sys.modules, "core.vectorestore", fake_module)
    monkeypatch.setattr(settings, "APP_MODE", "agent_course")

    vector_store = main.init_vector_store_sync()

    assert vector_store.collection_stats["status"] == "disabled"
    assert vector_store.hybrid_search("RAG") == []
