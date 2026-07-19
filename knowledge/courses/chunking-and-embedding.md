# Chunking And Embedding

Chunking turns long course material into smaller retrievable units. Embedding turns each unit into a vector so semantic search can retrieve related content.

Bad chunking causes two common learning failures:

- The retrieved chunk is too small and misses the surrounding explanation.
- The retrieved chunk is too large and hides the exact answer inside noise.

For AI engineering courses, chunking should preserve lesson titles, code blocks, error messages, and important configuration names. A good chunk carries metadata such as `course_id`, `lesson_id`, `source_type`, `topic`, `tags`, and `source_path`.

Chunking changes must be evaluated. If a new strategy improves one demo question but hurts recall on the evaluation set, it should not be treated as a real improvement.
