## Context

The repository currently implements a generic FastAPI RAG app with document ingestion, Milvus retrieval, reranking, a LangGraph flow, evaluation utilities, and a static frontend. The new target is an Agent / LLM course assistant that answers conceptual course questions, codebase questions, environment errors, FAQ items, and learning-path questions.

## Goals / Non-Goals

**Goals:**

- Build a narrow MVP that answers FAQ, course, code, and error questions with citations or clarification/refusal.
- Add a deep `QAOrchestrator` module so callers do not need to know routing, retrieval, gating, and trace details.
- Add code RAG MVP with Python AST symbol extraction and exact-first code search.
- Record a trace for every answer.
- Add a manual evaluation set and runner for route accuracy and basic answer behavior.

**Non-Goals:**

- Do not implement RAPTOR, LightRAG, GraphRAG, HippoRAG, ColBERT, multimodal layout RAG, or long-context routing in MVP.
- Do not create a new frontend framework.
- Do not add SaaS multi-tenancy, payment, CRM, or live-course management.

## Decisions

### Decision: Keep One FastAPI App

Use the existing FastAPI app and add focused modules under `core/` and `ingestion/`. A single app reduces setup risk and keeps the first local run achievable.

Alternative considered: split backend services by retrieval type. Rejected because the MVP needs reliable local verification more than service decomposition.

### Decision: Route Before Retrieval

Every query first passes through `core.intent_router.route_query()`. Route-specific retrieval prevents code, FAQ, and error questions from polluting one shared vector search path.

Alternative considered: one vector index and one prompt. Rejected because code and error questions require exact identifiers, source paths, and line numbers.

### Decision: Use Evidence Packet And Gate

Retrieval returns an `EvidencePacket`, then `retrieval_gate.decide_evidence()` decides accept, retry, clarify, or refuse. This keeps hallucination control before generation.

Alternative considered: tell the LLM to only answer from context. Rejected because prompt instructions alone do not provide a testable quality gate.

### Decision: Code RAG Starts With Python AST

The MVP extracts Python classes/functions/imports with the standard `ast` module and exact-first ranking. This gives code-aware citations without adding tree-sitter or a code graph dependency.

Alternative considered: index raw code chunks only. Rejected because raw chunks do not provide symbol names or stable line references.

### Decision: Trace Is Part Of The Answer Result

`QAResult.trace` carries route, decision, candidates, citations, and latency. Persistence can be added through the existing database layer without changing the answer interface.

Alternative considered: rely on logs only. Rejected because logs are not structured enough for evaluation and failure analysis.

## Risks / Trade-offs

- Rule-based routing may misclassify ambiguous queries → tests cover common routes, and Phase 2 can add model-based routing.
- AST code RAG only handles Python initially → enough for the current repository; tree-sitter is a Phase 2 option.
- In-memory matcher tests do not prove Milvus behavior → keeps MVP verifiable before heavy dependency repair.
- A deterministic MVP generator may feel less impressive → generation can be delegated to the existing LLM path after evidence selection is reliable.

## Migration Plan

1. Add OpenSpec and tests.
2. Repair dependencies and local compile baseline.
3. Add schemas and new core modules behind tests.
4. Wire `RAGService` through `QAOrchestrator`.
5. Run targeted tests and local smoke checks.

Rollback is a branch reset or reverting the new modules and service wiring. Existing legacy retrieval code remains available until the final product cleanup task.
