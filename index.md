---
type: Project
title: Finance Department AI Agent
description: 4-phase rollout for finance agent SaaS: AP coding, bank rec, flux narratives, expense compliance, vendor onboarding. Beachhead: AP invoice coding (15h/wk saved).
status: Active
tags: [finance, agent, saas, client-proposal, ai-agents]
timestamp: 2026-07-04T00:00:00Z
---

# PROJ-006 — Finance Department AI Agent

AI Agents are the new SaaS. Agent SaaS sells work your team no longer does.

## 4-Phase Rollout

| Phase | Timeline | Goal | Gate |
|-------|----------|------|------|
| 0. Discovery | Week 1 | Pick beachhead workflow; baseline metrics | Ranked list + sponsor sign-off |
| 1. MVP Agent | Weeks 1-3 | 1 workflow, shadow mode, >90% accuracy | >=90% match, >=50% time saved |
| 2. Production | Weeks 4-6 | SLA-grade, monitored, "virtual analyst" | 99.5% uptime, <30s latency |
| 3. Expand | Weeks 7-12 | 4-5 workflows on shared infra | Portfolio ROI dashboard |

## Beachhead: AP Invoice Coding & Routing

High volume, medium judgment, high error cost. Saves 15h/wk, low effort.

## Architecture

Context layer (policies, COA, approval matrices) + Tools (ERP API, Email/Slack, PDF Parse) + Orchestration (LangGraph/CrewAI, checkpoints, HITL). Provider-agnostic.

## Connections

- Related: [[AI-139]] — AI Agents are the new SaaS framework
