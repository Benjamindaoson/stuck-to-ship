## ADDED Requirements

### Requirement: Single evidence orchestration path
The system SHALL route every non-chat answer attempt through one retrieval, safety, grading, citation, generation, and trace path.

#### Scenario: Exact FAQ match uses the unified path
- **WHEN** a learner asks a question that exactly matches a stored FAQ
- **THEN** the FAQ evidence passes through the shared safety, grading, citation, and trace stages before an answer is returned

#### Scenario: Streaming and non-streaming parity
- **WHEN** the same query is submitted to streaming and non-streaming answer endpoints
- **THEN** both paths use the same route, retrieval plan, evidence decision, citations, and terminal outcome

### Requirement: Normalized evidence contract
Every retriever SHALL return evidence with stable identity, text, source path, source type, modality, exact location, raw scores, retrieval strategy, and security metadata.

#### Scenario: Code evidence normalization
- **WHEN** AST retrieval finds a Python symbol
- **THEN** the normalized evidence includes its file path, start line, end line, symbol type, exact-match score, and `code` modality

#### Scenario: Missing source identity
- **WHEN** a retriever returns a candidate without a stable source path or evidence identity
- **THEN** the system excludes that candidate from answer generation and records the exclusion in the trace

### Requirement: Hybrid retrieval and fusion
Course and uploaded-document retrieval SHALL combine dense and sparse candidates, deduplicate them by stable evidence identity, and preserve source-specific scores through fusion.

#### Scenario: Semantic and exact term evidence
- **WHEN** a query contains both a conceptual phrase and an exact API or configuration name
- **THEN** the candidate set includes eligible results from both dense and sparse retrieval before reranking

#### Scenario: Duplicate candidate
- **WHEN** dense and sparse retrieval return the same evidence identity
- **THEN** fusion emits one candidate containing both raw scores and its fused rank

### Requirement: Shared reranking and corrective grading
The system SHALL rerank fused candidates and SHALL decide `accept`, `retry`, `clarify`, or `abstain` before generation.

#### Scenario: Sufficient evidence
- **WHEN** reranked evidence meets confidence, source, safety, and coverage requirements
- **THEN** the grader returns `accept` and only accepted evidence enters answer generation

#### Scenario: Recoverable coverage gap
- **WHEN** required subqueries or modalities are missing and a retry remains
- **THEN** the grader returns `retry` with a structured repair reason and retrieval suggestion

#### Scenario: Retry budget exhausted
- **WHEN** evidence remains insufficient after two retries
- **THEN** the system returns clarification or refusal without unsupported generation

### Requirement: Evidence safety and access control
The system SHALL apply document ACL and prompt-injection filtering to evidence from every retriever before grading or generation.

#### Scenario: Unauthorized graph neighbor
- **WHEN** graph traversal reaches evidence that the requesting user cannot access
- **THEN** the system excludes the evidence and does not expose its content or relationship in citations or trace output

#### Scenario: Injection in extracted visual text
- **WHEN** OCR or VLM-extracted text contains prompt-injection instructions
- **THEN** the system blocks the evidence and records a redacted safety reason

### Requirement: Graceful retrieval degradation
The system SHALL preserve safe answer behavior when an optional retriever or model is unavailable.

#### Scenario: External Milvus unavailable
- **WHEN** dense retrieval is unavailable but local sparse or exact retrieval remains available
- **THEN** the system uses the available adapters, records the degraded mode, and still applies the evidence grader

#### Scenario: Reranker unavailable in enforce mode
- **WHEN** the reranker is unavailable and enforcement is enabled
- **THEN** the system abstains instead of treating fusion scores as accepted evidence
