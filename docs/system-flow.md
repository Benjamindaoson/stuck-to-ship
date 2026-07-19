# StuckToShip 系统流程

本文档描述当前 MVP 的真实运行流程，避免和旧项目骨架混淆。

## 启动流程

入口文件：`main.py`

```text
uvicorn main:app
  -> create_app()
      -> 配置 CORS 和 API Key 中间件
      -> 注册 /api/v1 路由
      -> 挂载 static/index.html
      -> startup 初始化业务数据库
```

可用入口：

| 入口 | 用途 |
|---|---|
| `/` | Web UI |
| `/health` | 健康检查 |
| `/api/v1/rag/ask` | 非流式问答 |
| `/api/v1/rag/ask-stream` | SSE 流式问答 |
| `/api/v1/documents/list` | 文档列表 |

如果配置了 `STUCKTOSHIP_API_KEYS`，所有 `/api/` 请求都需要 `Authorization: Bearer <key>` 或 `X-API-Key`。

## 问答流程

```text
Web UI or API client
  -> api/rag.py
      -> services/rag_service.py
          -> core/qa_orchestrator.py
              -> faq/error pre-match
              -> intent routing
              -> course/code/error/faq retrieval
              -> prompt injection guard
              -> document ACL filter
              -> retrieval gate
              -> answer with citations
```

## 数据流

```text
course_pack/
  courses/*.md|*.txt
  faq/*.jsonl
  errors/*.jsonl
  eval/*.jsonl
      |
      v
scripts/edu_rag.py import-course
      |
      v
knowledge/
  courses/
  faq/
  errors/
data/agent_course_eval/
```

导入后会生成 `knowledge/course_manifest.json`，记录导入文件、数量和时间。

## 安全流程

```text
request
  -> API Key middleware
  -> QAOrchestrator(user_id)
      -> retrieve candidates
      -> access_control.access_denial_reason()
      -> prompt_injection.detect_prompt_injection()
      -> build allowed evidence packet
      -> answer or abstain
```

安全能力：

- API Key 保护生产 API。
- 文档 front matter 可声明 `visibility` 和 `allowed_users`。
- 检索证据进入生成前会过滤文档内提示词注入。
- 被过滤的证据写入 trace，便于审计。

## 评估流程

```text
data/agent_course_eval/*.jsonl
  -> python -m evaluation.agent_course_eval --file ... --json
      -> QAOrchestrator
      -> route accuracy
      -> answer/refusal check
      -> source/reference check
```

当前评估集覆盖 course、code、faq、error、learning_path、clarify 和拒答问题。

## 部署流程

本地开发：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8010
```

生产模板：

```powershell
$env:STUCKTOSHIP_API_KEYS="replace-with-a-long-random-key"
docker compose -f docker-compose.production.yml up --build
```

生产建议接外部 Milvus/Zilliz 或独立 Milvus Standalone，不建议在 Windows 本地用 Milvus Lite 验证生产检索。
