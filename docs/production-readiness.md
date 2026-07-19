# Production Readiness

These are the pieces that cannot be created inside the repository.

## What you still need

| Item | What to provide | Where it goes |
|---|---|---|
| Real course data | lessons, project code, verified FAQ, error recipes, eval cases | `knowledge/` or `scripts/edu_rag.py import-course` |
| LLM API key | DeepSeek, OpenAI, DashScope, or another OpenAI-compatible service | `DEEPSEEK_API_KEY` or `LLM_API_KEY` |
| API access key | a long random key for users or your frontend | `STUCKTOSHIP_API_KEYS` |
| Server and domain | VM/container host plus DNS and HTTPS | cloud provider / reverse proxy |
| Milvus/Zilliz | production vector endpoint | `STUCKTOSHIP_MILVUS_URI` |

## DeepSeek

```text
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-flash
```

If your shell already has `DEEPSEEK_API_KEY`, the app will use it when `LLM_API_KEY` is not set.

## What is ready now

```powershell
Copy-Item .env.production.example .env.production
notepad .env.production
.\.venv\Scripts\python.exe scripts\check_production_ready.py --env-file .env.production
```

The check does not contact paid services. It only catches missing placeholders, missing local data paths, and missing deployment files.

## Minimal server deploy

```powershell
$env:STUCKTOSHIP_API_KEYS="replace-with-long-random-api-key"
docker compose -f docker-compose.production.yml up -d --build
```

Then put a reverse proxy with HTTPS in front of port `8000`.

Skipped for now: Kubernetes, multi-region deploy, managed secrets, and autoscaling. Add them only after real users or data volume require them.
