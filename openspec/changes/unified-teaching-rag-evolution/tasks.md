# Unified Teaching RAG Evolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one production-evaluable teaching RAG engine that combines Hybrid, Graph, Agentic, Code, FAQ/Error, and Multimodal evidence behind shared corrective grading and automated evaluation.

**Architecture:** Preserve `RAGService.ask()` and `ask_stream()` as the external seam. Replace the internal early-return split with one LangGraph path whose retrieval adapters emit `EvidenceCandidate`, then share fusion, ACL/injection filtering, reranking, corrective grading, generation, citation, trace, and evaluation behavior.

**Tech Stack:** Python 3.12, FastAPI, LangGraph, Milvus, BM25, sentence-transformers, SQLAlchemy/SQLite, Pydantic, pytest, and OpenAI-compatible text/vision models.

## Global Constraints

- Use only the project-local `.venv`; never install project dependencies into global Python.
- Keep `/api/v1/rag/ask` and `/api/v1/rag/ask-stream` backward compatible.
- Keep Windows text-only development functional without Milvus Lite, GPU, or a vision model.
- Apply ACL, prompt-injection filtering, corrective grading, citations, and trace capture to every retrieval adapter.
- Limit planner execution to three tool calls and corrective retrieval to two retries.
- Add no graph database until SQLite graph benchmarks demonstrate a requirement.
- Add no visual retrieval model until the text-first visual baseline is measured.

---

## 1. Baseline And Contract Lock

- [x] 1.1 Run `openspec validate unified-teaching-rag-evolution --strict` and fix every proposal, design, spec, or task validation error before implementation.
- [x] 1.2 Run `.\.venv\Scripts\python.exe -m pytest -q` and store the exact baseline test count and warnings in `docs/unified-rag-baseline.md`.
- [x] 1.3 Add frozen parity cases for course, learning path, code, FAQ, error, clarify, refusal, streaming, ACL, and prompt injection in `test/test_unified_rag_parity.py`.
- [x] 1.4 Run `.\.venv\Scripts\python.exe -m pytest test/test_unified_rag_parity.py -q` and confirm the fixtures describe current behavior before changing orchestration.

## 2. Unified Evidence Contracts And One Answer Path

- [x] 2.1 Add failing contract tests in `test/test_retrieval_contracts.py` for `RetrievalQuery`, `EvidenceCandidate`, stable evidence identity, location metadata, and adapter protocol behavior.
- [x] 2.2 Create `core/retrieval/contracts.py` with the exact interfaces defined in `design.md`, using frozen dataclasses and `typing.Protocol` without adding a dependency.
- [x] 2.3 Create adapter tests in `test/test_retrieval_adapters.py` that normalize existing course, AST, FAQ, and error results without losing source paths, lines, scores, ACL, or injection metadata.
- [x] 2.4 Create `core/retrieval/adapters.py` as thin adapters over `search_course_docs`, `search_code_symbols`, `match_faq`, and `match_error_recipe`; do not duplicate their matching implementations.
- [x] 2.5 Add failing tests in `test/test_evidence_fusion.py` for deduplication by stable identity, preservation of raw scores, and deterministic merged ordering.
- [x] 2.6 Create `core/retrieval/engine.py` with `async retrieve(plan: RetrievalPlan) -> EvidenceSet`, using registered adapters, ACL/injection filtering, fusion, reranking, and the existing quality gate.
- [x] 2.7 Update `core/state.py` so one `RAGState` carries normalized evidence, selected tools, planner budget, gate decision, citations, and redacted trace fields.
- [x] 2.8 Update `core/graph.py` to execute exact FAQ/error/code fast paths inside the graph and ensure every accepted answer passes the same grader and finalizer.
- [x] 2.9 Remove the `QAOrchestrator` early-return branch from `services/rag_service.py` only after non-streaming and streaming parity tests pass; keep the public response shape unchanged.
- [x] 2.10 Run `.\.venv\Scripts\python.exe -m pytest test/test_unified_rag_parity.py test/test_retrieval_contracts.py test/test_retrieval_adapters.py test/test_evidence_fusion.py test/test_rag_service_orchestrator.py -q` and commit the one-path migration.

## 3. Hybrid Retrieval As The Default Backbone

- [ ] 3.1 Add labeled dense-only, sparse-only, mixed semantic/exact, duplicate, no-hit, and degraded-Milvus cases to `data/test_sets/unified_retrieval_v1.jsonl`.
- [ ] 3.2 Add failing integration tests in `test/test_unified_hybrid_retrieval.py` proving course queries use dense and BM25 candidates, RRF fusion, stable deduplication, and cross-encoder reranking.
- [ ] 3.3 Adapt `core/vectorestore.py` and `core/nodes/retriever.py` to return normalized candidates with `dense_raw_score`, `sparse_raw_score`, `fusion_score`, query variant, and index version.
- [ ] 3.4 Make course and uploaded-document retrieval use the unified Hybrid adapter while keeping deterministic local sparse fallback when external Milvus is unavailable.
- [ ] 3.5 Fuse AST exact matches with Hybrid code candidates without treating raw code as an undifferentiated document chunk.
- [ ] 3.6 Extend `evaluation/retrieval_evaluator.py` to report Recall@10, MRR, nDCG@10, duplicate rate, false accept rate, per-adapter latency, and degraded-mode results.
- [ ] 3.7 Benchmark the existing embedding/reranker against BGE-M3 and any selected reranker candidate on the frozen set; change defaults only when quality improves without violating latency gates.
- [ ] 3.8 Run `.\.venv\Scripts\python.exe -m evaluation.cli retrieval-evaluate --from-file data/test_sets/unified_retrieval_v1.jsonl` and require Recall@10 `>= 0.85` and nDCG@10 `>= 0.70` before enabling unified Hybrid retrieval by default.
- [ ] 3.9 Run the full pytest suite and local `/health`, `/api/v1/rag/ask`, and `/api/v1/rag/ask-stream` smoke checks, then commit the Hybrid phase.

## 4. Teaching Concept And Code GraphRAG

- [ ] 4.1 Add failing schema tests in `test/test_teaching_graph_models.py` for supported node/edge types, source evidence, snapshot version, source hash, and uniqueness constraints.
- [ ] 4.2 Add `KnowledgeGraphNode` and `KnowledgeGraphEdge` SQLAlchemy models plus indexes and uniqueness constraints in `models/db_models.py`; use the existing SQLite database and initialization flow.
- [ ] 4.3 Add graph extraction fixtures for course prerequisites, lesson links, Python imports/calls, configuration references, and error causes/fixes under `test/fixtures/teaching_graph/`.
- [ ] 4.4 Create `ingestion/graph_indexer.py` to build validated nodes/edges from explicit course metadata, Python AST, configuration files, and error recipes; reject unsupported or source-less facts.
- [ ] 4.5 Add `scripts/edu_rag.py graph-build` and `graph-stats` commands that write a reproducible graph manifest containing source hashes, counts, failures, and snapshot version.
- [ ] 4.6 Add failing retrieval tests in `test/test_teaching_graph_retrieval.py` for entity linking, one-hop prerequisites, two-hop code/config paths, access filtering, unsupported entities, and traversal limits.
- [ ] 4.7 Create `core/retrieval/graph.py` with `GraphRetriever.retrieve()` using bounded one- or two-hop traversal and normalized path evidence.
- [ ] 4.8 Register `GraphRetriever` behind `ENABLE_GRAPH_RETRIEVAL=false`, fuse graph candidates with Hybrid candidates, and include path plus underlying file/line citations.
- [ ] 4.9 Add at least 30 graph-required and 30 Hybrid-control questions to `data/test_sets/teaching_graph_v1.jsonl` with expected entities, paths, sources, and answer behavior.
- [ ] 4.10 Extend evaluation to report entity-link accuracy, path accuracy, multi-hop answer correctness, graph-only latency, and Hybrid-only baseline comparison.
- [ ] 4.11 Enable Graph retrieval only when multi-hop correctness is `>= 0.80` and at least 10 percentage points above Hybrid-only correctness on graph-required held-out cases; run the full suite and commit the graph phase.

## 5. Bounded Agentic RAG

- [ ] 5.1 Add failing plan-schema tests in `test/test_agent_planner.py` for deterministic fast paths, registered tool names, three-call budget, two-retry budget, timeouts, and terminal reasons.
- [ ] 5.2 Create `core/planner.py` with frozen `ToolCall` and `RetrievalPlan` types, deterministic FAQ/error/code/simple-course planning, model-plan validation, and safe fallback planning.
- [ ] 5.3 Register `hybrid`, `code`, `graph`, `faq`, `error`, and later `multimodal` tools in code; reject user-supplied tools, URLs, commands, and executable arguments.
- [ ] 5.4 Update `core/graph.py` with planner, parallel tool execution, fusion, corrective repair, clarification, abstention, and explicit budget-exhausted terminal nodes.
- [ ] 5.5 Add trace tests proving plan source, selected tools, redacted arguments, latency, budget usage, grader reason, retry strategy, and terminal reason are recorded for every answer attempt.
- [ ] 5.6 Add planner failure tests for malformed model output, timeout, unavailable model, tool exception, partial parallel failure, and exhausted budget.
- [ ] 5.7 Add at least 50 planner cases to `data/test_sets/agent_planner_v1.jsonl` covering fast paths, multi-source comparisons, graph-required questions, ambiguity, refusal, and adversarial tool instructions.
- [ ] 5.8 Add planner evaluation for tool-selection accuracy, unnecessary tool-call rate, completion rate, retry rate, latency, and model usage.
- [ ] 5.9 Enable `ENABLE_AGENT_PLANNER` for complex queries only after tool-selection accuracy is `>= 0.90`, all budget assertions pass, and deterministic routes show no parity regression; run the full suite and commit the Agentic phase.

## 6. Multimodal Course Evidence

- [ ] 6.1 Define and test a course asset manifest in `test/test_multimodal_manifest.py` for PDF pages, PPT slides, images, transcript segments, keyframes, ACL, page/slide/timestamp locations, source hashes, and extractor versions.
- [ ] 6.2 Add only the minimal proven dependencies for PDF page rendering and PPT extraction to `requirements.txt`, install them in `.venv`, and record exact version bounds after a clean-environment install test.
- [ ] 6.3 Extend `ingestion/loader.py` and create `ingestion/multimodal.py` to emit text plus location-preserving visual/transcript assets without requiring a vision model during basic ingestion.
- [ ] 6.4 Extend `ingestion/pipeline.py` and document import endpoints/CLI to store asset metadata, generated files, failures, and index version in an ingestion manifest.
- [ ] 6.5 Add failing tests in `test/test_multimodal_retrieval.py` for slide text retrieval, diagram-required retrieval, code screenshot metadata, transcript timestamp retrieval, private assets, and missing vision capability.
- [ ] 6.6 Create `core/retrieval/multimodal.py` with text-first asset retrieval and an optional OpenAI-compatible vision adapter invoked only for top-ranked accessible visual assets.
- [ ] 6.7 Normalize multimodal evidence into the shared candidate contract and return page, slide, image, or timestamp citations through both answer endpoints.
- [ ] 6.8 Add at least 50 labeled visual questions and assets under `data/test_sets/multimodal_v1/`, separating development and held-out page retrieval cases.
- [ ] 6.9 Benchmark text-first retrieval against an optional ColPali-style adapter; enable visual embeddings only if held-out page Recall@5 improves by at least 10 percentage points and deployment latency remains within limits.
- [ ] 6.10 Enable `ENABLE_MULTIMODAL_RETRIEVAL` only when page Recall@5 is `>= 0.80`, ACL/injection tests pass, and text-only local fallback remains green; run the full suite and commit the multimodal phase.

## 7. Continuous Evaluation And Versioning

- [ ] 7.1 Add failing persistence tests in `test/test_evaluation_versioning.py` for dataset, chunk, embedding, reranker, planner, prompt, graph, multimodal extractor, application, latency, and usage versions.
- [ ] 7.2 Extend `EvaluationRecord` and evaluation serialization with versioned run metadata while preserving existing evaluation history responses.
- [ ] 7.3 Add a release evaluator that combines route/tool, retrieval, citation, groundedness, refusal, graph, multimodal, latency, and usage reports without hiding failed cases behind averages.
- [ ] 7.4 Add answerable, ambiguous, unanswerable, unsafe, unauthorized, stale, and conflicting-evidence cases until the frozen release retrieval set contains at least 100 labeled cases.
- [ ] 7.5 Add reviewed feedback promotion so negative learner feedback creates a review record containing query, redacted trace, evidence, and configuration but cannot automatically publish FAQ, error, graph, or evaluation data.
- [ ] 7.6 Add CLI commands for baseline creation, candidate comparison, release-gate execution, and JSON/Markdown report export under `evaluation/cli.py` and `scripts/edu_rag.py`.
- [ ] 7.7 Run the release evaluator and require every threshold in `design.md`; store the report under `data/evaluation_reports/` with configuration hashes, then commit the evaluation phase.

## 8. Product, Security, Performance, And Release Verification

- [ ] 8.1 Update `static/index.html` to display selected tools, evidence modality, graph path, page/slide/timestamp citations, corrective decisions, and degraded capabilities without exposing private trace content.
- [ ] 8.2 Update `.env.example`, `.env.production.example`, `docs/system-flow.md`, production readiness checks, and both READMEs with rollout flags, data requirements, benchmark commands, and capability status.
- [ ] 8.3 Extend security tests so API auth, ACL, prompt-injection filtering, trace redaction, and unauthorized citation checks cover every new adapter and modality.
- [ ] 8.4 Run concurrency and latency benchmarks in the documented production environment; require first-token P95 `<= 3s` and full-answer P95 `<= 15s`, or keep the failing capability disabled.
- [ ] 8.5 Run `.\.venv\Scripts\python.exe -m pytest -q`, `.\.venv\Scripts\python.exe -m compileall -q .`, all release evaluation commands, and `openspec validate unified-teaching-rag-evolution --strict`.
- [ ] 8.6 Start `.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8010`, verify `/health`, one Hybrid question, one graph question, one Agentic multi-source question, one multimodal question, one refusal, SSE completion, and the primary browser flow.
- [ ] 8.7 Review the final diff for hardcoded secrets, accidental private data, unbounded loops, unnecessary dependencies, stale duplicate orchestration, and undocumented migration flags before the release commit.
