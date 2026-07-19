# Course Data Requirements

StuckToShip needs real course data from the course owner. Code can provide the importer and validation, but it cannot invent private lessons, student questions, or verified fixes.

## Minimum Useful Dataset

For a useful private MVP, prepare:

| Data | Minimum | Target | Format | Destination |
|---|---:|---:|---|---|
| Course lessons | 10-30 | 50+ | Markdown/TXT | `knowledge/courses/` |
| Real student questions | 50-100 | 300+ | JSONL FAQ | `knowledge/faq/` |
| Error recipes | 20-50 | 100+ | JSONL | `knowledge/errors/` |
| Evaluation cases | 50-100 | 300+ | JSONL | `data/agent_course_eval/` |
| Course project codebases | 1-3 | 5+ | Source repo | `CODE_RAG_ROOTS` |

## Folder Layout For Import

Create a source folder like this:

```text
my-course-data/
  courses/
    outline.md
    lesson-01-rag.md
    lesson-02-embedding.md
  faq/
    faq.jsonl
  errors/
    errors.jsonl
  eval/
    manual.jsonl
```

Import it:

```powershell
.\.venv\Scripts\python.exe scripts\edu_rag.py import-course C:\path\to\my-course-data --overwrite
```

The importer validates JSONL first, copies files into `knowledge/` and `data/`, and writes `knowledge/course_manifest.json`.

## Course Lessons

Use Markdown or TXT. One lesson per file is best.

Recommended front matter:

```markdown
---
course_id: agent-rag
lesson_id: lesson-03
source_type: course_note
topic: retrieval
tags: [rag, embedding, milvus]
visibility: public
---

# RAG Basics

...
```

For private lessons:

```markdown
---
visibility: private
allowed_users: [u1, u2]
---
```

Current ACL support is file-metadata oriented for course evidence loaded into the orchestrator. If private documents are imported through other ingestion paths, the same metadata must be preserved before production use.

## FAQ JSONL

Required fields:

```json
{"question":"How do I configure DashScope API Key?","answer":"Set LLM_API_KEY in .env.","category":"setup","tags":["dashscope","api-key"],"source":"course-faq"}
```

Required:

- `question`
- `answer`

Recommended:

- `category`
- `tags`
- `priority`
- `source`

## Error Recipe JSONL

Required fields:

```json
{"error_pattern":"ModuleNotFoundError: No module named pymilvus","symptom":"Import fails on startup.","cause":"The active virtual environment does not have pymilvus installed.","fix_steps":["Activate .venv","Run pip install -r requirements.txt"],"verify_command":"python -c \"import pymilvus\"","tags":["python","milvus","dependency"]}
```

Required:

- `error_pattern`
- `symptom`
- `cause`
- `fix_steps`

Recommended:

- `verify_command`
- `related_files`
- `tags`

## Evaluation JSONL

Required fields:

```json
{"question":"What problem does RAG solve?","expected_route":"course","should_answer":true,"expected_sources":["lesson-01-rag.md"],"notes":"Must mention retrieval before generation."}
```

Required:

- `question`
- `expected_route`
- `should_answer`

Recommended:

- `expected_sources`
- `expected_answer`
- `notes`

Use these route values:

```text
faq
course
code
error
learning_path
clarify
out_of_scope
```

## Best Data Sources

Use these first:

1. Your own course slides, lesson notes, transcripts, and project walkthroughs.
2. Real student questions from chat groups, issues, DMs, live Q&A, and assignment feedback.
3. Verified setup and runtime errors from real logs.
4. Project README, config files, startup scripts, and important source files.
5. Short summaries of official docs with source URLs and checked dates.

Avoid:

- Random scraped blog content.
- Unauthorized paid-course material.
- Duplicated low-quality Q&A.
- Unverified fixes copied from forums.

## Data Cleaning Rules

- Remove personal information from student questions.
- Merge duplicate questions.
- Keep exact error messages.
- Keep verified fix commands.
- Preserve source file paths.
- Add course/lesson/topic metadata early.
- Put any untrusted copied text through prompt-injection review.

## MVP Acceptance Bar

Before calling the dataset useful, run:

```powershell
.\.venv\Scripts\python.exe scripts\edu_rag.py agent-eval --file data/agent_course_eval/manual_v1.jsonl --json
.\.venv\Scripts\python.exe -m pytest -q
```

A useful first private dataset should answer most real course questions with citations and refuse questions that are not covered by the course.
