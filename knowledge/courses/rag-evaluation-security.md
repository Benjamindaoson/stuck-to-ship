# RAG Evaluation And Security

RAG quality must be measured at multiple points:

- intent routing accuracy
- retrieval recall
- citation support
- refusal accuracy
- answer usefulness
- latency

Security matters because retrieved documents are untrusted input. A document can contain instructions such as "ignore previous instructions" or "reveal the system prompt". These instructions must not override system behavior.

Production RAG also needs access control. The retriever must not return private course documents to users who are not allowed to see them. It is not enough to hide the citation after generation; private evidence must be filtered before the answer is created.

Every safety failure should produce a trace so developers can reproduce and fix it.
