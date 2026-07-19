# RAG evaluation and reranking

A reranker scores the top retrieval candidates again using the full query and each candidate passage. Candidate retrieval should be broad and fast; reranking should be more precise. Use a reranker when the first-stage retriever returns plausible but noisy results, and measure the latency cost.

Faithfulness means the answer is supported by the retrieved evidence. A faithful answer may be incomplete, but it should not invent unsupported facts. Evaluation should track route accuracy, citation coverage, retrieval recall, answer faithfulness, refusal quality, and latency.

Corrective RAG checks whether retrieved evidence is strong enough before generation. If the evidence is weak, the system can rewrite the query, retrieve again, ask for clarification, or refuse. This lowers hallucination risk because bad context is not blindly sent into the prompt.

A production RAG trace should record the query, route, rewritten queries, retrieved documents, scores, prompt version, model, answer, citations, latency, and feedback. Without traces, debugging answer quality is mostly guesswork.
