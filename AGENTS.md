# AGENTS.md — finance-demo-agent

This is the source of truth for AI agent instructions on this project.

## Project

Finance Department AI Agent (PROJ-006). 4-phase rollout for finance agent SaaS: AP coding, bank rec, flux narratives, expense compliance, vendor onboarding. Beachhead: AP invoice coding (15h/wk saved).

## Rules

- Follow the phased rollout: Discovery → MVP → Production → Expand
- Each phase has explicit gate criteria that must be met before proceeding
- Provider-agnostic architecture — core/ must have zero framework imports
- All ERP calls route through `core/tools/erp_adapter.py`

## See Also

- `index.md` — Rollout phases, architecture, connections to wiki
- `CLAUDE.md` — Claude Code instructions (example)
