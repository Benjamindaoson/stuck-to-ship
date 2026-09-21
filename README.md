# StuckToShip — Migrated into AI Talents Learning OS

> **Status: SUPERSEDED · migration source only**

StuckToShip is no longer maintained as an independent learning product.

Its durable Tutor capabilities have been migrated into **AI Talents Learning OS**:

https://github.com/Benjamindaoson/huisen-ai-adaptive-algorithm-coach

The standalone StuckToShip UI and product shell are now considered historical. New AI+Education product work should go to AI Talents Learning OS.

## What was migrated

| StuckToShip capability | AI Talents Learning OS target |
|---|---|
| Intent routing | `services/tutor-runtime/intent-router.ts` |
| Course RAG | `services/tutor-runtime/retrievers.ts` |
| Learning-path retrieval | `services/tutor-runtime/retrievers.ts` |
| Code RAG | `services/tutor-runtime/retrievers.ts` |
| Error diagnosis | `services/tutor-runtime/retrievers.ts` |
| FAQ retrieval | `services/tutor-runtime/retrievers.ts` |
| Evidence gate | `services/tutor-runtime/evidence-gate.ts` |
| Citation output | `contracts/tutor-runtime.ts` |
| QA orchestration | `services/tutor-runtime/runtime.ts` |
| QA / retrieval trace | unified `EvidenceEvent` stream |

## New canonical Tutor flow

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

The migrated Tutor does **not** directly update learner mastery.

```text
Tutor explanation
      ≠
Mastery evidence
```

Mastery in AI Talents Learning OS is updated from verified learner outcomes such as code execution, transfer tasks, delayed retests, and project evidence.

## Why this repository is still here

The repository remains available temporarily for:

- migration provenance;
- regression comparison;
- historical implementation reference;
- verification that no unique capability was lost during consolidation.

No new standalone product features should be added here.

## Canonical project

**AI Talents Learning OS**  
Multi-Agent Adaptive Learning System for LLM, RAG, Agents & Embodied AI

Current repository:

https://github.com/Benjamindaoson/huisen-ai-adaptive-algorithm-coach

> The repository slug is legacy; the product identity is **AI Talents Learning OS**.
