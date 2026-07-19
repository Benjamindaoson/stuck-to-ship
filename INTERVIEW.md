# StuckToShip 面试讲解手册

StuckToShip 是一个面向 AI 工程学习场景的课程助教。它解决的不是“再做一个聊天框”，而是学生在学 RAG、Agent、LangGraph、MCP、向量库和课程项目时，经常卡在概念、代码、环境和学习路径之间来回切换的问题。

## 一分钟介绍

我做了一个 AI 工程课程助教，核心目标是把学生从“卡住”带到“能继续做”。系统会先判断问题类型，比如概念解释、代码解释、环境报错、FAQ 或学习路径，然后到对应的数据源里找证据，最后给出带引用的回答。

这个项目的关键不只是 RAG，而是课程场景下的可控答疑链路：回答要通俗，但必须有出处；能回答就基于证据回答，证据不足就拒答或追问；遇到高频问题和报错，不浪费大模型，而是优先命中 FAQ 和错误配方。

## 核心价值

| 痛点 | StuckToShip 的做法 |
|---|---|
| 学生听不懂概念 | 用课程讲义和官方文档摘要解释，回答带来源 |
| 项目源码看不懂 | 单独做代码路由和代码检索 |
| 环境报错反复出现 | 把错误原文、原因、修复步骤、验证命令沉淀成 error recipe |
| 大模型容易胡说 | 检索门控和引用约束，证据不足则拒答 |
| 课程资料会更新 | 课程数据独立导入，评估集可回归 |
| 生产 RAG 有安全风险 | API Key、文档 ACL、Prompt Injection 过滤 |

## 技术栈

| 层 | 技术 |
|---|---|
| API | FastAPI |
| 编排 | QAOrchestrator, 可扩展 LangGraph |
| 检索 | FAQ matcher、error matcher、course retriever、code retriever |
| 安全 | API Key middleware、document ACL、prompt injection guard |
| 数据 | Markdown/TXT、JSONL、SQLite、Milvus/Zilliz 生产接口 |
| 评估 | JSONL golden set、route accuracy、引用和拒答回归 |
| 部署 | Dockerfile、docker-compose.production.yml |

## 架构讲法

```text
用户问题
  -> IntentRouter
      -> faq
      -> error
      -> code
      -> learning_path
      -> course
      -> clarify
  -> 对应 Retriever
  -> EvidencePacket
      -> Prompt Injection 过滤
      -> Document ACL 过滤
  -> RetrievalGate
  -> 带引用回答或拒答
```

这个设计的重点是分路由和证据治理。课程问答、代码问答和报错排查不是同一种检索问题，混到一个向量库里容易慢、乱、错。

## 可以重点展示的模块

1. 课程数据导入 CLI：`scripts/edu_rag.py import-course`
2. FAQ/Error 轻量命中：减少延迟和模型成本。
3. EvidencePacket：把安全、权限、引用统一到生成前。
4. Evaluation CLI：用固定 JSONL 评估路由、拒答和引用。
5. Docker 生产模板：能从本地演示走向生产部署。
6. Web UI：直接从“概念、代码、报错、下一步”四个学习卡点进入。

## 面试时主动承认的边界

当前版本是可运行 MVP，不是完整商业 SaaS。还没有接真实私有课程后台、支付、CRM、完整 RBAC、多模态 PPT/视频检索和 AST 级代码图检索。

但它已经把生产级 RAG 的关键底座打出来了：数据导入、分路由检索、证据引用、安全过滤、基础权限、评估回归和部署模板。

## 下一步升级路线

| 阶段 | 目标 |
|---|---|
| P1 | 导入真实课程数据，做 trace viewer 和 feedback-to-FAQ |
| P2 | 接 Milvus hybrid search、reranker、AST code graph |
| P3 | 做 RAPTOR/LightRAG 概念关系检索 |
| P4 | 接多模态 PPT/架构图检索和课程链接推荐 |

## 常见追问回答

**为什么不直接用 Dify/FastGPT？**

平台适合快速搭 Bot，但这个项目展示的是课程场景下的 RAG 工程能力：路由、证据治理、ACL、安全过滤、评估和反馈闭环都需要自己掌控。

**为什么不是纯向量检索？**

报错、API 名、文件名、函数名和环境变量很依赖精确匹配。课程概念适合语义检索，代码和报错更需要关键词、结构信息和规则。

**如何证明回答可靠？**

每次回答都要求有引用；证据不足会拒答；评估集持续回归路由、引用和拒答；trace 记录被过滤证据和决策原因。

**数据从哪里来？**

最重要的是课程讲义、项目源码、真实学员问题、真实报错和老师整理的标准答案。公开资料只能作为补充，不能替代课程私有数据。
