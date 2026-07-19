# MCP Tool Integration

MCP lets an assistant access external tools and data sources through a structured protocol. In an AI engineering course, MCP is often introduced after learners understand normal tool calling.

A safe MCP integration needs:

- clear tool schemas
- permission boundaries
- predictable error handling
- trace logs for tool calls
- refusal when the tool result is not enough

MCP should not be added just to make a demo look advanced. It is useful when the course assistant needs to query a real system such as documents, tasks, repositories, or internal records.

For a first RAG tutor, MCP is a later module. Course retrieval, code retrieval, evaluation, and safety gates should work first.
