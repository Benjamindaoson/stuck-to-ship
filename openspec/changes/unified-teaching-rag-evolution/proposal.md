## Why

StuckToShip currently has a focused course/code/FAQ/error orchestrator and a separate LangGraph retrieval pipeline. This split prevents the course tutor from consistently using the existing hybrid retrieval, reranking, corrective retries, and evaluation machinery, while relationship-heavy and visual course questions remain unsupported.

The next product phase needs one teaching RAG engine that chooses the right evidence path for concept, code, error, graph, image, slide, and video questions without exposing multiple RAG modes to learners.

## What Changes

- Replace the two-path answer flow with one evidence-gated orchestration path.
- Normalize Hybrid, Code, Graph, FAQ/Error, and Multimodal retrieval output into one evidence contract.
- Make dense retrieval, sparse retrieval, fusion, deduplication, cross-encoder reranking, and corrective grading the default retrieval backbone.
- Add a teaching knowledge graph for AI concept prerequisites, code calls, configuration dependencies, errors, lessons, and exercises.
- Add a bounded Agent Planner that selects only registered retrieval tools, enforces call/retry budgets, and records every decision in the trace.
- Add multimodal course evidence ingestion and retrieval for PDF/PPT pages, diagrams, code screenshots, transcripts, keyframes, and timestamped video segments.
- Expand automated evaluation from route accuracy to retrieval quality, citation correctness, groundedness, refusal quality, graph multi-hop quality, multimodal page recall, latency, and cost.
- Preserve the existing FastAPI endpoints and SSE response shape while enriching trace and citation metadata.

## Capabilities

### New Capabilities

- `unified-evidence-retrieval`: One normalized retrieval, fusion, reranking, safety, and corrective-grading path for every answer.
- `teaching-knowledge-graph`: Concept and code graph ingestion, bounded graph traversal, graph evidence, and path citations.
- `bounded-agent-planning`: Deterministic fast paths plus budget-bounded tool planning for complex learner questions.
- `multimodal-course-evidence`: Ingestion, retrieval, reasoning, and citations for visual and timestamped course assets.
- `continuous-rag-evaluation`: Versioned datasets, offline/online quality metrics, regression gates, and baseline comparisons.

### Modified Capabilities

None. The earlier `agent-course-rag` capability remains the completed MVP baseline; this change adds next-stage capabilities without rewriting that change.

## Impact

- Core orchestration: `services/rag_service.py`, `core/qa_orchestrator.py`, `core/graph.py`, and `core/state.py`.
- Retrieval: `core/vectorestore.py`, `core/nodes/retriever.py`, `core/reranker.py`, `core/retrieval_quality.py`, and new focused modules under `core/retrieval/`.
- Graph data: new graph node/edge models, deterministic course/code extractors, and a graph retrieval module.
- Multimodal ingestion: `ingestion/loader.py`, `ingestion/pipeline.py`, document schemas, storage metadata, and new visual/transcript adapters.
- Evaluation: new versioned datasets and metrics under `evaluation/` and `data/test_sets/`.
- Configuration and deployment: opt-in rollout flags, model/index version metadata, and optional multimodal runtime dependencies.
- Public API paths remain stable; response data gains richer evidence location, modality, planner, and evaluation trace fields.
