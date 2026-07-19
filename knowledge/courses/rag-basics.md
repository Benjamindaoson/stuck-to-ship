# RAG basics for LLM applications

Retrieval augmented generation (RAG) is a pattern where the system retrieves trusted course evidence before asking the language model to answer. The model should use the retrieved context as grounding, cite the source, and avoid making claims when evidence is missing.

Embeddings support semantic vector search: similar meanings can match even when the words differ. Sparse search supports exact terms such as API names, error strings, function names, and configuration keys. A strong technical QA system usually combines both, because dense retrieval is good at meaning while sparse retrieval is good at precision.

Chunk size changes the tradeoff between recall, precision, context pollution, and latency. Small chunks are precise but may miss cross-paragraph context. Large chunks preserve context but can bring unrelated text into the prompt and make answers less faithful.

Query expansion creates alternate phrasings of the same question. It helps when students use vague wording, but it can add noise when the original question already contains exact identifiers such as `MILVUS_URI`, `ModuleNotFoundError`, or a function name.
