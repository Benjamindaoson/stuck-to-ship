# StuckToShip — 已迁移至 AI Talents Learning OS

> **状态：SUPERSEDED · 仅保留为迁移来源与历史参考**

StuckToShip 不再作为独立学习产品继续维护。

其核心 Tutor 能力已经迁移到 **AI Talents Learning OS**：

https://github.com/Benjamindaoson/huisen-ai-adaptive-algorithm-coach

原来的 StuckToShip 独立 UI 与产品壳现在只作为历史实现保留；后续 AI+Education 产品开发统一进入 AI Talents Learning OS。

## 已迁移能力

| StuckToShip | AI Talents Learning OS |
|---|---|
| Intent Routing | `services/tutor-runtime/intent-router.ts` |
| Course RAG | `services/tutor-runtime/retrievers.ts` |
| Learning Path Retrieval | `services/tutor-runtime/retrievers.ts` |
| Code RAG | `services/tutor-runtime/retrievers.ts` |
| Error Diagnosis | `services/tutor-runtime/retrievers.ts` |
| FAQ Retrieval | `services/tutor-runtime/retrievers.ts` |
| Evidence Gate | `services/tutor-runtime/evidence-gate.ts` |
| Citation | `contracts/tutor-runtime.ts` |
| QA Orchestration | `services/tutor-runtime/runtime.ts` |
| Retrieval / QA Trace | 统一 `EvidenceEvent` |

## 新的统一 Tutor 流程

```text
Learner Question
      ↓
Intent Router
      ↓
Course / Code / Error / FAQ Retrieval
      ↓
Evidence Gate
      ↓
Grounded Tutor Action
      ↓
Citation + Trace
      ↓
EvidenceEvent
```

Tutor 的解释不会直接提升 Learner Mastery。

```text
Tutor Explanation
      ≠
Mastery Evidence
```

能力状态只根据真实学习结果更新，例如代码执行、迁移任务、延迟复测与项目证据。

## 为什么暂时保留这个仓库

用于：

- 迁移来源追溯；
- 回归对照；
- 历史实现参考；
- 确认整合过程没有遗漏唯一能力。

不再在这里新增独立产品功能。

## Canonical Product

**AI Talents Learning OS**  
面向 LLM、RAG、Agent 与具身智能的多智能体自适应学习系统。

当前仓库：

https://github.com/Benjamindaoson/huisen-ai-adaptive-algorithm-coach

> 当前 GitHub slug 仍为历史名称，但产品统一名称已经是 **AI Talents Learning OS**。
