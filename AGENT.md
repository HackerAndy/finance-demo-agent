# AGENT.md — Finance Demo Agent Root Intent Layer

**Synthesis:** AI-074 (Intent Layers), PROJ-006

> **What this file is:** A token-efficient architectural summary for AI agents. Instead of crawling files repeatedly, the agent reads this first to understand structure, rules, and patterns. One per major directory; update after significant refactors.

---

## What This Project Does

Beachhead AI agent for invoice processing & GL coding (Phase 1 of PROJ-006). Single focused workflow: ingest invoice PDF → extract fields → match PO → code to GL → create ERP entry → human review queue. Built with provider-agnostic core (zero framework imports), standalone eval harness, thin LangGraph orchestration, and ERP/email interfaces.

---

## Directory Map

| Directory | Role |
|-----------|------|
| `core/tools/` | Invoice extraction, PO matching, GL coding, ERP adapter (plain Python) |
| `core/validators/` | Schema validation, GL code master list, business rules (deterministic) |
| `core/prompts/` | System prompts per stage as versioned YAML files |
| `core/policies/` | Approval thresholds, escalation rules (config-driven) |
| `core/models.py` | Pydantic schemas for Invoice, PO, GLEntry, AuditRecord |
| `evals/` | Standalone evaluation harness — runs against core/, not LangGraph |
| `evals/golden_set/` | 50-100 labeled invoices + expected outputs |
| `orchestration/` | ONLY directory that imports LangGraph (~10-15% of code) |
| `orchestration/graph.py` | Nodes, edges, state schema |
| `orchestration/checkpointer.py` | Postgres persistence |
| `orchestration/interrupts.py` | HITL pause/resume at $ gates |
| `interfaces/` | ERP adapter, email listener, Slack approvals, review UI |

---

## Critical Rules (Read Before Touching Anything)

- **Zero framework imports in `core/` and `evals/`.** Never import `langgraph`, `langchain`, or any orchestration framework outside `orchestration/`. Enforced by CI lint check.
- **All ERP calls go through `core/tools/erp_adapter.py`.** Never call ERP APIs directly from orchestration or interfaces.
- **GL codes validated against master list.** Every coded invoice must pass `validators.gl_codes.validate(gl_code)` before ERP submission.
- **Dollar thresholds from config, never hardcoded.** Human review gates read from `core/policies/thresholds.yaml`.
- **Pydantic for all data crossing boundaries.** Invoice, PO, GLEntry, AuditRecord are Pydantic models in `core/models.py`.

---

## Anti-Patterns (Things AI Commonly Gets Wrong Here)

- **Don't add business logic in LangGraph nodes.** Nodes should be thin glue: call core tool → validate → return. Business logic lives in `core/tools/`.
- **Don't put ERP-specific code in `core/tools/`.** Use `erp_adapter.py` seam; swap adapter for different ERP.
- **Don't hardcode dollar thresholds in prompts or nodes.** Read from `policies/thresholds.yaml` — business users change these quarterly.
- **Don't create new utility files in `core/` root.** Utilities belong in `core/tools/` if shared across 3+ modules, otherwise co-locate with the code using them.
- **Don't skip validators in eval runs.** The eval harness must run the same validators as production to catch drift.

**Why this matters:** These patterns look correct to an LLM because they're common in tutorials, but they violate the architectural decisions that make this harness portable and testable. Documenting them prevents reinventing reasonable-but-wrong approaches.

---

## Global Invariants

- Every invoice follows the `{ invoice_id, vendor, amount, line_items, gl_codes, status, audit_trail }` envelope shape
- All timestamps are UTC, stored as ISO 8601 strings
- Authentication checked at interface layer — never inside core tools
- Golden set eval runs on every PR; accuracy < 90% on top 20 GL accounts = fail
- Audit record written for every state transition (received → extracted → matched → coded → submitted → approved/rejected)

---

## Key Entry Points

- `orchestration/graph.py` — LangGraph flow definition; start here to understand the workflow
- `core/tools/` — Business logic implementations; read to understand what each step does
- `core/validators/gl_codes.py` — GL master data and validation logic
- `core/policies/thresholds.yaml` — Business-configurable approval gates
- `evals/run_baseline.py` — Run golden set evaluation; produces accuracy/latency/cost report
- `interfaces/erp_adapter.py` — ERP contract; implement for new ERP integration

---

## Supplementary Tools

**Intent Layers (AGENT.md files) — Recommended**
- **Best for:** Most projects, especially existing codebases
- **How:** Document structure, rules, anti-patterns, invariants in readable markdown
- **Cost:** Human time to write once, then minimal maintenance
- **Benefit:** Forces you to articulate architecture; catches AI mistakes early
- **Maintenance:** Update after major refactors

**Code Review Graphs — For highly interconnected codebases**
- **Best for:** Large projects where blast radius analysis matters; complex dependency chains
- **How:** MCP server builds semantic graph (functions, imports, relationships)
- **Cost:** Initial setup + graph maintenance
- **Benefit:** Faster context retrieval; automated blast radius analysis
- **Trade-off:** More infrastructure; modest token savings; primarily speeds up discovery

**Recommendation:** Start with Intent Layers (AGENT.md). Only add Code Review Graphs if Claude frequently asks "what calls this?" or you're doing large refactors across interconnected modules.