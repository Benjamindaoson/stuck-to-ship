## ADDED Requirements

### Requirement: Query intent routing
The system SHALL classify every user query into one route before retrieval: `faq`, `course`, `code`, `error`, `learning_path`, `clarify`, or `out_of_scope`.

#### Scenario: Route code query
- **WHEN** the user asks where a Python function is defined
- **THEN** the system routes the query to `code`

#### Scenario: Clarify vague query
- **WHEN** the user asks an underspecified question such as "这个怎么弄？"
- **THEN** the system routes the query to `clarify`

### Requirement: Evidence-gated answers
The system SHALL return a cited answer only when retrieved evidence is present and has sufficient confidence.

#### Scenario: Missing evidence
- **WHEN** retrieval returns no evidence
- **THEN** the system asks for clarification or refuses instead of generating an unsupported answer

#### Scenario: Supported evidence
- **WHEN** retrieval returns evidence with a source path and acceptable score
- **THEN** the system allows answer generation and includes citations

### Requirement: Code RAG citations
The system SHALL answer code questions with file paths and line numbers when symbols are found.

#### Scenario: Python function found
- **WHEN** the user asks for a known Python function
- **THEN** the system returns the matching source path, symbol name, and start/end lines

### Requirement: Trace capture
The system SHALL produce a structured trace for every answer attempt.

#### Scenario: Trace produced
- **WHEN** the system answers, clarifies, or refuses a query
- **THEN** the result includes route, decision, candidates, citations, and latency fields

### Requirement: Course and learning path evidence
The system SHALL answer `course` and `learning_path` MVP queries from local course documents when matching course evidence exists.

#### Scenario: Course concept evidence found
- **WHEN** the user asks a RAG concept question covered by local course notes
- **THEN** the system returns an answer with at least one course citation

#### Scenario: Learning path evidence found
- **WHEN** the user asks what to learn next in the Agent RAG track
- **THEN** the system returns a learning path answer with at least one course citation

### Requirement: Streaming orchestration diagnostics
The system SHALL expose Agent course route, citations, and trace data through the streaming answer path.

#### Scenario: Streaming FAQ answer
- **WHEN** a FAQ query is answered by the Agent course orchestrator
- **THEN** the final SSE `done` event includes route, references, trace, latency, and session id

### Requirement: External Milvus configuration
The project SHALL include a Docker Compose configuration for running external Milvus when full vector retrieval is required.

#### Scenario: Milvus compose endpoint
- **WHEN** the Milvus Compose file is inspected
- **THEN** it exposes the standalone Milvus endpoint on port 19530

### Requirement: MVP evaluation
The system SHALL provide a manual JSONL evaluation set and runner for route accuracy and answer behavior.

#### Scenario: Load manual evaluation set
- **WHEN** the evaluator loads the manual dataset
- **THEN** it reads at least 30 cases with question, expected route, and should-answer fields

### Requirement: Course data import
The system SHALL provide a local CLI importer that validates and copies course lessons, FAQ rows, error recipes, and evaluation cases into the project data layout.

#### Scenario: Import valid course assets
- **WHEN** a source directory contains `courses/`, `faq/`, `errors/`, or `eval/` assets
- **THEN** the importer validates required fields, copies supported files, and writes an import manifest

#### Scenario: Reject invalid FAQ rows
- **WHEN** a FAQ JSONL row is missing `question` or `answer`
- **THEN** the importer fails with a useful validation error before copying partial data

### Requirement: Retrieved context safety
The system SHALL block retrieved evidence that appears to contain prompt-injection instructions before answer generation.

#### Scenario: Malicious retrieved note
- **WHEN** a retrieved course note tells the model to ignore previous instructions or reveal system prompts
- **THEN** the system excludes that evidence and refuses or asks for better context if no safe evidence remains

### Requirement: Production API protection
The system SHALL support opt-in API key authentication for `/api/` routes.

#### Scenario: API keys configured
- **WHEN** production API keys are configured and a request omits a valid `Authorization: Bearer` or `X-API-Key` header
- **THEN** the API returns `401`

### Requirement: Document ACL filtering
The system SHALL filter private retrieved evidence by user id before it can be cited.

#### Scenario: Private lesson denied
- **WHEN** a private course document allows only user `u1`
- **THEN** a query from user `u2` cannot cite that document
