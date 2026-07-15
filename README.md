# Finance Demo Agent - Beachhead Workflow

A focused AI agent for one specific finance workflow: **Invoice Processing & GL Coding**.

## Project Scope (Beachhead Only)

This is Phase 1 (Weeks 1-3) of the Finance Department AI Agent Plan (PROJ-006).
**Single workflow**: Ingest invoice PDF → Extract fields → Match PO → Code to GL → Create ERP entry → Human review queue.

## Architecture

```
finance-demo-agent/
├── core/
│   ├── tools/          # Invoice extraction, PO matching, GL coding
│   ├── validators/     # Schema validation, business rules
│   ├── prompts/        # System prompts per stage
│   └── policies/       # Approval thresholds, escalation rules
├── evals/
│   └── golden_set/     # 50-100 labeled invoices for eval
├── orchestration/      # LangGraph flow definition
└── interfaces/         # ERP adapter, email listener, review UI
```

## Quick Start

```bash
# 1. Set up virtual env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Add golden set invoices
cp evals/golden_set/templates/* evals/golden_set/

# 3. Run evaluation baseline
python -m evals.run_baseline

# 4. Start orchestration server
python -m orchestration.server
```

## Beachhead Success Criteria (Week 3)

- [ ] 95% field extraction accuracy on golden set
- [ ] 90% PO match rate
- [ ] 85% correct GL coding (top 20 accounts)
- [ ] < 30s end-to-end latency
- [ ] Human review queue functional

## Related

- Parent Plan: [[PROJ-006]] — Finance Department AI Agent Plan
- Phase 2: [[PROJ-006-finance-department-ai-agent-plan.md]] — Weeks 4-12 expansion