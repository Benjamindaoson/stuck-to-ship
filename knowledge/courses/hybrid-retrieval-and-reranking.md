# Hybrid Retrieval And Reranking

Dense vector search is useful for conceptual questions. Sparse keyword search is better for exact terms such as function names, API names, environment variables, and error messages.

Hybrid retrieval combines both:

- dense retrieval for semantic similarity
- sparse retrieval for exact identifiers
- metadata filtering for course, lesson, visibility, source type, and user access

Reranking is the second-stage sort. It takes a wider candidate set and selects the few passages most likely to support the answer. Reranking reduces irrelevant context and can lower generation cost by sending fewer chunks to the LLM.

In a course assistant, code questions and error questions should not rely only on dense vectors. They need exact matching and citations.
