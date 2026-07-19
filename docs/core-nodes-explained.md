# QA 核心节点说明

StuckToShip 的问答链路围绕“先判断问题类型，再找可信证据，最后基于证据回答”设计。当前 MVP 没有强行堆复杂 Agent，而是把关键节点做成可测试、可替换的模块。

## 1. IntentRouter

文件：`core/intent_router.py`

职责：把用户问题路由到合适的数据源。

| 路由 | 典型问题 |
|---|---|
| `faq` | “需要 GPU 吗？”、“API Key 怎么配？” |
| `error` | `ModuleNotFoundError`、Milvus 连接失败、启动报错 |
| `code` | “main.py 怎么启动？”、“这个函数在哪里调用？” |
| `learning_path` | “我下一步该学什么？” |
| `course` | “RAG 和微调有什么区别？” |
| `clarify` | 信息不足，需要追问 |

## 2. Matcher 层

文件：

- `core/faq_matcher.py`
- `core/error_matcher.py`

职责：对高频问题和报错走轻量命中，减少 LLM 调用，降低延迟。

设计原则：

- FAQ 适合标准答案。
- Error recipe 适合固定排障步骤。
- 只有低置信度时才进入通用课程/代码检索。

## 3. Retriever 层

文件：

- `core/course_retriever.py`
- `core/code_retriever.py`

职责：从课程资料和项目源码里召回候选证据。

当前 MVP 使用轻量文本检索和元数据打分，后续可以替换为 Milvus hybrid search、reranker、AST code graph，但接口不需要大改。

## 4. EvidencePacket

文件：`core/evidence.py`

职责：把候选证据整理成可引用上下文，并在进入生成前做安全过滤。

过滤规则：

- 命中文档 Prompt Injection 指令的证据会被阻断。
- 文档 ACL 不允许当前用户访问的证据会被阻断。
- 最终回答只使用通过过滤的证据。
- trace 中会记录 `blocked_evidence`，方便排查为什么没有引用某些文档。

## 5. RetrievalGate

文件：`core/retrieval_gate.py`

职责：判断证据是否足够支持回答。

输出：

- `accept`: 证据足够，生成答案。
- `abstain`: 证据不足或全部被安全/权限过滤，拒答或追问。

## 6. QAOrchestrator

文件：`core/qa_orchestrator.py`

职责：串联完整问答链路。

```text
query
  -> FAQ/Error pre-match
  -> IntentRouter
  -> Retriever
  -> EvidencePacket
  -> RetrievalGate
  -> grounded answer or refusal
  -> trace
```

它是后续升级 LangGraph、复杂 query decomposition、反馈闭环和 trace viewer 的核心扩展点。
