## ADDED Requirements

### Requirement: Deterministic fast-path planning
The system SHALL create deterministic retrieval plans for exact FAQ, known error, direct code symbol, and simple course queries without an LLM planner call.

#### Scenario: Direct code lookup
- **WHEN** a learner asks where a known function is defined
- **THEN** the plan selects the code retriever directly and does not call the LLM planner

### Requirement: Registered retrieval tools
The planner SHALL select tools only from the code-registered retrieval tool set and SHALL NOT execute user-supplied tool names, URLs, shell commands, or Python code.

#### Scenario: Tool instruction in user query
- **WHEN** a learner message asks the planner to execute an unregistered command or tool
- **THEN** the planner ignores the requested executable action and records a safety decision

### Requirement: Bounded planning budget
Every plan SHALL contain at most three tool calls, and the corrective loop SHALL perform at most two retrieval retries.

#### Scenario: Planner proposes too many tools
- **WHEN** a model-generated plan contains more than three tool calls
- **THEN** plan validation rejects or truncates it to a safe deterministic plan before execution

#### Scenario: Budget exhausted
- **WHEN** all tool and retry budgets are exhausted without sufficient evidence
- **THEN** the workflow terminates with clarification or refusal

### Requirement: Parallel independent retrieval
The system SHALL execute independent retrieval tool calls concurrently while preserving deterministic evidence merging and trace order.

#### Scenario: Concept and code comparison
- **WHEN** a plan requires independent course and code retrieval
- **THEN** both tools may execute concurrently and their evidence is merged by stable identity before reranking

### Requirement: Planner clarification
The planner SHALL request clarification before retrieval when the requested course topic, code target, error context, or visual asset is too ambiguous to form a safe plan.

#### Scenario: Missing code target
- **WHEN** a learner asks "why does this fail" without code, error text, file, or prior context
- **THEN** the system asks for the missing target instead of calling unrelated retrieval tools

### Requirement: Planner trace
Every answer attempt SHALL record plan source, selected tools, tool arguments, timing, budget consumption, repair decisions, and terminal reason without exposing secrets.

#### Scenario: Corrective tool switch
- **WHEN** weak text evidence causes the planner to add graph or multimodal retrieval
- **THEN** the trace records the grader reason, selected replacement tool, and remaining budget

### Requirement: Planner failure isolation
An unavailable planner model SHALL NOT prevent deterministic fast paths or safe refusal.

#### Scenario: Planner timeout
- **WHEN** the LLM planner times out for a complex query
- **THEN** the system uses a deterministic fallback plan within the same tool budget or refuses if no safe plan exists
