# Agent systems and external memory

An LLM context window is temporary working memory. It only contains the messages and context included in the current request. External memory stores information outside the prompt so an Agent can retrieve it later.

Agents need external memory when tasks span many steps, sessions, tools, files, or user preferences. Retrieval memory is useful for facts and course notes; working memory is useful for the current reasoning step; long-term memory is useful for stable preferences and project state.

Tool calling is the general ability for a model to request structured actions. Function calling is one API style for representing those tool calls with names and JSON arguments. In production systems, the hard parts are schema design, validation, retries, permission boundaries, and tracing.

Prompt injection in RAG happens when retrieved content tries to override system instructions or steal secrets. The assistant should treat retrieved text as untrusted data, separate instructions from evidence, and prefer allowlisted tools and explicit citations.
