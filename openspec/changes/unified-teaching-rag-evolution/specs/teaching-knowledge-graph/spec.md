## ADDED Requirements

### Requirement: Teaching graph schema
The system SHALL represent validated AI learning and code relationships using the supported node and edge types defined by the design.

#### Scenario: Concept prerequisite
- **WHEN** course metadata states that embeddings are a prerequisite for vector retrieval
- **THEN** the graph stores source-linked concept nodes and a `prerequisite_of` edge

#### Scenario: Unsupported relationship type
- **WHEN** an extractor proposes an edge type outside the supported schema
- **THEN** graph ingestion rejects the edge and reports the source record and validation reason

### Requirement: Source-grounded graph ingestion
Every graph node and edge SHALL retain the source evidence and graph snapshot version from which it was derived.

#### Scenario: Python call relationship
- **WHEN** deterministic AST analysis finds that one indexed function calls another resolvable symbol
- **THEN** the graph stores a `calls` edge with caller/callee file and line evidence

#### Scenario: LLM-proposed relationship
- **WHEN** an LLM proposes a concept relationship without valid source evidence
- **THEN** the proposal is not published to the retrieval graph

### Requirement: Bounded graph retrieval
Graph retrieval SHALL link query entities and traverse at most two hops unless a future reviewed specification changes the limit.

#### Scenario: Learning prerequisite question
- **WHEN** a learner asks what to study before LangGraph state management
- **THEN** graph retrieval returns the linked prerequisite path and source evidence within two hops

#### Scenario: No linked entity
- **WHEN** the query cannot be linked to a graph node with sufficient confidence
- **THEN** graph retrieval returns no candidate rather than traversing unrelated high-degree nodes

### Requirement: Graph and Hybrid fusion
Graph evidence SHALL join the same normalized candidate set, reranking, safety, and corrective grading used by other retrievers.

#### Scenario: Graph is supplementary
- **WHEN** both graph and Hybrid retrieval produce evidence for a comparison question
- **THEN** fusion preserves graph path provenance and text evidence before reranking

#### Scenario: Graph path lacks document support
- **WHEN** a graph path exists but none of its nodes or edges has accessible source evidence
- **THEN** the path cannot support answer generation

### Requirement: Graph citations
Answers using graph evidence SHALL cite both the relationship path and the underlying source locations.

#### Scenario: Code configuration explanation
- **WHEN** an answer explains that a function is configured by an environment setting
- **THEN** the citation includes the symbol line, configuration source, and relationship path used

### Requirement: Rebuildable graph snapshots
Graph ingestion SHALL produce a versioned, reproducible snapshot that can be rebuilt from validated course, code, configuration, and error sources.

#### Scenario: Source changes
- **WHEN** a source file changes and graph ingestion runs again
- **THEN** stale facts from that source are replaced and the new snapshot records source hashes and ingestion time
