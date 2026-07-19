# Agent Memory And State

Agent memory is not the same as putting all chat history into the prompt. Useful memory is scoped, verified, and relevant to the next task.

For course learning, safe memory can include:

- completed lessons
- repeated errors
- preferred explanation level
- project environment facts confirmed by the learner

Unsafe memory includes guessed facts, unsupported technical conclusions, and secrets. A course assistant should not remember API keys or private credentials.

State should be visible in traces. When the answer depends on memory or prior context, the system should show what state was used and why.
