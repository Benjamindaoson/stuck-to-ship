# Agent Course Knowledge Layout

Store MVP knowledge under this directory:

```text
knowledge/
  courses/        # course outlines, lessons, PPT text, transcripts
  projects/       # README, startup notes, key files, configs
  faq/            # FAQ CSV or JSONL
  errors/         # structured error recipes
  assignments/    # assignment prompts and hint rules
  eval/           # manually reviewed evaluation cases
```

Minimum MVP data:

```text
10 course documents
1 course project
50 FAQ rows
20 error recipes
30 evaluation questions
```

Current seed data is intentionally smaller and runnable:

```text
4 course documents
5 FAQ rows
5 error recipes
32 evaluation questions
project code symbols loaded from CODE_RAG_ROOTS
```

Add private course assets under `knowledge/courses/` first. Use external Milvus only when you need uploaded PDF/Markdown/TXT document ingestion and full vector retrieval.
