## 1. Specification And Baseline

- [x] 1.1 Validate OpenSpec change `agent-course-rag-mvp`.
- [x] 1.2 Capture current dependency dry-run failure and compile baseline.
- [x] 1.3 Repair dependency constraints and MVP settings.

## 2. Product Surface

- [x] 2.1 Hide unfinished legacy analytics and knowledge routes from the MVP surface.
- [x] 2.2 Update visible product wording to Agent course assistant.

## 3. Core Contracts

- [x] 3.1 Add source type, citation, FAQ, error recipe, and trace schemas.
- [x] 3.2 Add intent router and clarification gate.
- [x] 3.3 Add evidence packet and retrieval gate.

## 4. Retrieval Routes

- [x] 4.1 Add Python AST code symbol extraction.
- [x] 4.2 Add exact-first code symbol search.
- [x] 4.3 Add FAQ matcher.
- [x] 4.4 Add error recipe matcher.

## 5. Orchestration

- [x] 5.1 Add `QAOrchestrator` answer interface.
- [x] 5.2 Wire RAG service to use `QAOrchestrator`.
- [x] 5.3 Ensure every answer result includes trace data.

## 6. Evaluation And Smoke

- [x] 6.1 Add 30-case Agent course manual eval set.
- [x] 6.2 Add MVP eval runner.
- [x] 6.3 Run targeted pytest suite, compileall, and local app smoke checks.

## 7. Blocker Closure

- [x] 7.1 Add seed course documents that produce citations for `course` and `learning_path`.
- [x] 7.2 Wire Agent course orchestration into streaming responses.
- [x] 7.3 Add route, citation, and trace diagnostics to the frontend.
- [x] 7.4 Add Docker Milvus configuration for full vector retrieval.
- [x] 7.5 Add global rule requiring project-local virtual environments.

## 8. Release Readiness Closure

- [x] 8.1 Add validated course-data import CLI for lessons, FAQ, error recipes, and eval cases.
- [x] 8.2 Document the exact real-course data required for a useful private deployment.
- [x] 8.3 Add retrieved-document prompt-injection filtering before answer generation.
- [x] 8.4 Add opt-in API key authentication for production API routes.
- [x] 8.5 Add basic document ACL filtering for private course evidence.
- [x] 8.6 Refresh the public UI and app naming to StuckToShip.
- [x] 8.7 Add a production Docker deployment template.
