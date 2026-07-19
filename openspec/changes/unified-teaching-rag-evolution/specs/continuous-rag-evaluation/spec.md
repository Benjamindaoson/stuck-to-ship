## ADDED Requirements

### Requirement: Versioned evaluation runs
Every evaluation run SHALL record dataset, chunk, embedding, reranker, planner, prompt, graph snapshot, multimodal extractor, and application versions with its metrics.

#### Scenario: Comparable run
- **WHEN** an evaluator runs the same frozen dataset against a new retrieval configuration
- **THEN** the report identifies both configurations and supports baseline comparison without overwriting prior results

### Requirement: Retrieval evaluation coverage
The project SHALL maintain at least 100 labeled retrieval cases covering concepts, exact technical terms, code, errors, multi-hop relationships, ambiguity, refusal, and visual evidence before enabling all advanced retrieval modes by default.

#### Scenario: Incomplete dataset
- **WHEN** fewer than 100 valid labeled retrieval cases are supplied to the release evaluation
- **THEN** the evaluator reports the coverage failure and does not mark the retrieval release gate as passed

### Requirement: Quality release gates
The evaluator SHALL calculate and enforce the quality thresholds stated in the design for route/tool selection, Hybrid retrieval, citations, groundedness, refusal, graph multi-hop questions, and multimodal page retrieval.

#### Scenario: Citation precision regression
- **WHEN** citation precision falls below `0.95` on the frozen release set
- **THEN** the release evaluation fails and reports the affected cases

#### Scenario: Graph baseline comparison
- **WHEN** Graph retrieval is evaluated for release
- **THEN** the report compares graph-enabled correctness with the Hybrid-only baseline on graph-required questions

### Requirement: Latency and usage measurement
The system SHALL record retrieval, rerank, planner, vision, generation, first-token, total latency, and available model usage for evaluated answers.

#### Scenario: Streaming latency gate
- **WHEN** the documented production benchmark is run
- **THEN** the report includes first-token and full-answer P50/P95 values and fails if the stated P95 limits are exceeded

### Requirement: Failure-oriented datasets
Evaluation data SHALL include answerable, ambiguous, unanswerable, unsafe, unauthorized, stale, and conflicting-evidence cases.

#### Scenario: Unauthorized evidence case
- **WHEN** an evaluation user lacks access to the only relevant private source
- **THEN** the expected behavior is refusal or clarification with zero private citations

### Requirement: Reviewed feedback promotion
Learner feedback and production failures SHALL enter a review queue before they become FAQ records, error recipes, graph facts, or frozen evaluation cases.

#### Scenario: Negative feedback
- **WHEN** a learner marks an answer incorrect
- **THEN** the system stores the query, trace, evidence, and feedback for review without automatically publishing model-generated corrections
