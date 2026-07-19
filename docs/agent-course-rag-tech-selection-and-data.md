# StuckToShip: 技术选型与数据方案

StuckToShip 的目标不是做通用聊天机器人，而是解决 AI 工程课程里最常见的学习卡点：概念听不懂、代码看不懂、项目跑不通、不知道下一步学什么。系统必须回答得准、讲得清楚、有出处，并且能把失败问题沉淀成 FAQ、错误配方和评估集。

## MVP 边界

第一阶段只做五类问题：

| 路由 | 用户问题 | 主要数据源 |
|---|---|---|
| `course` | RAG、Agent、MCP、LangGraph 等概念解释 | 课程讲义、课程笔记、官方文档摘要 |
| `code` | 项目结构、启动流程、函数/模块职责 | README、源码、配置、脚本 |
| `error` | 环境、依赖、API、Milvus、启动报错 | 错误配方 JSONL、项目配置 |
| `faq` | 高频重复问题 | FAQ JSONL |
| `learning_path` | 学习顺序、下一步怎么做 | 课程大纲、章节目标 |

第一阶段不做完整 LMS、支付、CRM、直播、自动批改、复杂多租户运营后台。

## 技术选型

| 层 | 选择 | 原因 |
|---|---|---|
| 后端 | FastAPI | 轻量、异步友好、API 文档直接可用 |
| 编排 | Python QA Orchestrator, 后续可迁移 LangGraph | MVP 先把可测链路跑稳，再扩成图状态机 |
| 检索 | 课程/FAQ/错误/代码分路检索 | 课程答疑不是单一向量库问题，不同问题需要不同证据 |
| 向量库 | Milvus/Zilliz, 本地可用 Lite 或外部服务 | 面向生产保留可扩展向量检索能力 |
| 关键词检索 | 轻量 BM25/规则匹配 | 报错、文件名、API 名称不能只靠语义向量 |
| 重排 | 先规则分数，后续接 bge-reranker/ColBERT 类 late interaction | 控制 MVP 复杂度，同时保留升级方向 |
| LLM | OpenAI-compatible 接口 | 可切换 OpenAI、Qwen、DeepSeek、Ollama |
| 数据导入 | `scripts/edu_rag.py import-course` | 让课程资料、FAQ、错误配方、评估集有稳定入口 |
| 安全 | API Key、Prompt Injection 过滤、文档 ACL | RAG 的生产风险主要在越权检索和被文档注入带偏 |
| 评估 | JSONL golden set + 路由/引用/拒答回归 | 不靠主观感觉调 RAG |
| 部署 | Dockerfile + production compose | 本地可跑，生产可接外部 Milvus |

## 当前架构

```text
Web UI
  -> FastAPI
      -> API Key middleware
      -> RAG API
          -> RAGService
              -> QAOrchestrator
                  -> IntentRouter
                  -> FAQMatcher
                  -> ErrorMatcher
                  -> CourseRetriever
                  -> CodeRetriever
                  -> EvidencePacket
                      -> PromptInjectionGuard
                      -> DocumentACL
                  -> RetrievalGate
                  -> Grounded answer with citations
      -> Course import CLI
      -> Evaluation CLI

knowledge/
  courses/     course notes and project explainers
  faq/         high-frequency Q&A JSONL
  errors/      error recipes JSONL

data/agent_course_eval/
  manual_v1.jsonl
  manual_v2.jsonl
```

## 必须准备的数据

真实课程数据不能由代码凭空生成。代码现在已经提供导入入口和种子数据，但要做成真正可用产品，需要以下数据。

| 数据 | MVP 最低量 | 作品集目标量 | 用途 |
|---|---:|---:|---|
| 课程讲义/笔记 | 10-30 篇 | 50+ 篇 | 回答概念、原理、学习路径 |
| 真实学员问题 | 50-100 条 | 300+ 条 | FAQ、失败聚类、产品定位 |
| 报错解决方案 | 20-50 条 | 100+ 条 | 环境和项目运行问题快速命中 |
| 评估问题 | 50-100 条 | 300+ 条 | 回归测试、指标展示 |
| 课程项目代码库 | 1-3 个 | 5+ 个 | 代码解释、启动排查、作业辅助 |
| 官方文档摘要 | 5-20 篇 | 按课程扩展 | 版本化补充最新 API 知识 |

最有价值的数据不是网上随机文章，而是真实学员反复问的问题、真实报错、课程项目源码和老师整理过的标准答案。

## 数据获取顺序

1. 先整理课程已有素材：讲义、PPT 转文本、字幕、README、作业说明、项目代码。
2. 再整理真实问答：微信群、社群、直播答疑、私信、GitHub issue、作业反馈。
3. 把报错单独做成错误配方：错误原文、现象、原因、修复步骤、验证命令。
4. 从课程内容和真实问题中抽样做评估集，必须包含应该拒答或追问的问题。
5. 官方文档只做课程相关摘要，保留来源 URL、版本和更新时间。

## 导入格式

推荐把待导入数据放到一个独立目录：

```text
course_pack/
  courses/
    lesson-01-rag.md
    lesson-02-agent.md
  faq/
    faq.jsonl
  errors/
    errors.jsonl
  eval/
    manual_eval.jsonl
```

导入命令：

```powershell
.\.venv\Scripts\python.exe scripts\edu_rag.py import-course C:\path\to\course_pack --overwrite
```

详细字段规范见 [docs/course-data-requirements.md](./course-data-requirements.md)。

## 后续高含金量模块

| 模块 | 解决的问题 | 优先级 |
|---|---|---|
| Query decomposition | 多跳问题拆解，比如“Agent 调工具失败”同时涉及 schema、prompt、环境变量 | P1 |
| Retrieval trace viewer | 展示候选证据、过滤原因、引用来源、延迟 | P1 |
| Feedback-to-FAQ | 把低分回答和重复问题沉淀成 FAQ 草稿 | P1 |
| AST/code graph retrieval | 代码问题需要调用关系和配置依赖，不是普通文本相似度 | P2 |
| RAPTOR/层级摘要 | 长讲义需要先检索章节摘要，再下钻原文 | P2 |
| LightRAG/小型概念图 | Agent/RAG 概念依赖强，适合实体关系辅助检索 | P2 |
| ColBERT/late interaction | 报错、API 名、代码符号需要 token 级匹配 | P3 |
| Multimodal layout RAG | PPT、流程图、架构图需要版面和图片理解 | P3 |

## 验收指标

| 指标 | MVP 目标 |
|---|---:|
| 路由准确率 | >= 90% |
| 引用覆盖率 | 100% |
| FAQ 命中准确率 | >= 85% |
| 错误配方命中准确率 | >= 80% |
| 应拒答问题拒答率 | >= 80% |
| 本地回归评估可复现 | 100% |

当前代码已经能跑通 MVP 骨架。产品质量的上限接下来取决于真实课程数据、真实问题和持续评估闭环。
