# Public Learner Question Seeds

This file documents the first public-source learner-question seed set.

Dataset:

```text
data/learner_questions/public_ai_engineering_questions.jsonl
```

Scope:

- 60 normalized questions.
- Sources: public GitHub Issues and Stack Overflow questions.
- Domains: RAG, LangChain, LangGraph, LlamaIndex, Milvus, OpenAI API, MCP, Agent tooling, evaluation, memory, streaming, deployment errors.

Rules used:

- Questions are paraphrased and normalized for a course assistant.
- No usernames, personal data, comments, answers, or long post text are copied.
- Each row keeps `source_url` so a human can verify the public signal.
- These rows are not FAQ answers. They are raw demand signals and should be reviewed by a teacher or maintainer before becoming FAQ, eval, or error recipes.

Recommended next step:

```text
public_learner_question -> teacher review -> FAQ/error recipe/eval case
```

Minimum schema:

```json
{
  "id": "plq-001",
  "question": "normalized learner question",
  "category": "evaluation",
  "intent_hint": "course",
  "tags": ["rag", "evaluation"],
  "source_platform": "GitHub Issues",
  "source_url": "https://...",
  "license_note": "public_source_paraphrased"
}
```
