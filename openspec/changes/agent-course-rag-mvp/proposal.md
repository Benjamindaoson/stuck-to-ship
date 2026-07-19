## Why

The cloned project is a generic education RAG skeleton, but the target product is an Agent / LLM course assistant. The MVP needs a focused answer pipeline that can route questions across course notes, code, FAQ, and error data while producing citations, traces, and evaluation results.

## What Changes

- Replace legacy generic education product behavior with Agent / LLM course assistant behavior.
- Add intent routing for FAQ, course knowledge, code, error, learning-path, clarification, and out-of-scope requests.
- Add source-aware evidence packets and retrieval gates so unsupported answers clarify or refuse instead of hallucinating.
- Add a Python code RAG MVP using AST symbols and exact-first matching.
- Add FAQ and error recipe matching as first-class retrieval routes.
- Add trace data for every answer and a small manual evaluation runner.
- Keep RAPTOR, LightRAG, ColBERT, multimodal RAG, and long-context routing out of the MVP implementation.

## Capabilities

### New Capabilities

- `agent-course-rag`: Agent / LLM course assistant behavior, including routing, code RAG, evidence grounding, traces, and MVP evaluation.

### Modified Capabilities

None.

## Impact

- Affects FastAPI RAG endpoints, service orchestration, schemas, database models, ingestion, retrieval, tests, and docs.
- Adds local tests for routing, evidence gating, code indexing, matchers, orchestration, traces, and evaluation.
- Adds OpenSpec and Codex support files created by `openspec init`.
