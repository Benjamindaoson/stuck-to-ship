# Unified RAG Baseline

Date: 2026-07-19
Branch: `agent-course-rag-mvp`
Change: `unified-teaching-rag-evolution`

## Command

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Result

- Tests: 118 passed
- Warnings: 8
- Duration: 47.63s

## Warnings

- `StarletteDeprecationWarning`: FastAPI `TestClient` imports Starlette's deprecated `httpx` integration from `.venv\Lib\site-packages\fastapi\testclient.py:1`.
- `DeprecationWarning`: `langchain-community` sunset warning from `core\embeddings.py:1`.
- `DeprecationWarning`: SQLAlchemy calls `datetime.datetime.utcnow()` through dependency code.

## Purpose

This baseline locks the pre-migration behavior before moving the RAG orchestration toward one unified evidence path.
