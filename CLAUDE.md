# CLAUDE.md — Finance Demo Agent

**Synthesis:** PROJ-006, AI-139, AI-018, AI-134

---

> **For beachhead workflow:** Fill every `[FINANCE-SPECIFIC]` section, delete sections that don't apply, keep under 300 lines.
> **Test:** "Could a senior finance engineer infer this from reading the codebase?" If yes, delete it.

## Project Intent

**What it does:** Beachhead AI agent for invoice processing & GL coding — ingests invoice PDFs, extracts fields, matches POs, assigns GL codes, creates ERP entries, routes to human review queue.

**Why it matters:** Phase 1 of Finance Department AI Agent Plan (PROJ-006). Proves the "AI Agents are the new SaaS" model (AI-139) by replacing manual AP coding with measurable ROI: 90% time reduction, >85% accuracy on top 20 GL accounts.

**Stack:** Python 3.11+, LangGraph (orchestration only), Postgres (checkpointer), OpenRouter (multi-provider LLM), ERP REST API, email/Slack interfaces

**Non-obvious tooling:**
- `core/tools/erp_adapter.py` — ONLY place ERP calls live; swap for different ERP
- `core/validators/gl_codes.py` — Static GL master data; update quarterly from ERP export
- `core/policies/thresholds.yaml` — Dollar thresholds for human review; business-configurable

---

## The Four Core Rules

Apply to every response, every session. These eliminate 80% of AI coding failures.

### 1. Don't Assume — Surface Confusion
- If a requirement is ambiguous, list the interpretations before proceeding
- If a tradeoff exists (speed vs. correctness, pragmatism vs. purity), surface it
- Never silently choose one path when the human should decide
- Example: "I see two ways to interpret 'fast response times' — subsecond latency or quick time-to-first-byte. Which matters here?"

### 2. Minimum Code
- Write the smallest implementation that satisfies the goal
- No speculative abstractions, no "we might need this later"
- No refactoring unless explicitly requested
- Exception: fixing a bug may require refactoring if the code structure caused it
- Example: Don't extract a helper function unless the same logic appears twice

### 3. Surgical Precision
- Every changed line traces directly to the request
- If you touch a file, explain why each change is necessary
- Don't "clean up" adjacent code unless asked
- Resist bundling unrelated fixes (do one thing per commit)

### 4. Goal-Driven Verification
- Before claiming "done," verify the stated success criteria are met
- Test the golden path and edge cases if possible
- Don't stop at "code written" — confirm "goal achieved"
- Example: Running tests passing ≠ feature working in the real app

---

## Strategic vs. Tactical Boundary

Humans own strategy. AI owns tactics inside approved strategy.

### You (AI) Own
- Implementation inside approved module boundaries
- Boilerplate and scaffolding
- Test generation at defined seams
- Internal refactoring if it improves quality within scope
- Bug fixes without changing interfaces
- Documentation for code you write

### Humans Must Approve Before Acting
- Changing a public API, exported interface, or type signature
- Adding a new dependency (library, service, infrastructure)
- Database schema changes
- Deleting, moving, or renaming files (except obvious fixes)
- Any architectural decision
- Work that touches more than one module

**Decision flow:** If you hit a choice that falls in the "humans approve" list, stop and ask. Do not guess.

---

## Codebase Architecture

**Deep modules, not shallow.** Every module presents a simple interface hiding complex implementation.
- **Bad:** An `Invoice` module that exposes `vendor_id`, `amount`, `date`, `line_items`, `tax`, `currency`, `payment_terms`, `po_number`, `gl_code`, `approval_status` — too many concepts.
- **Good:** An `Invoice` module with `process(pdf_bytes)` and `get_status(invoice_id)` — the implementation is hidden.

**Seams at every boundary.** Database, HTTP, auth, clock, file system each get a seam with a prod adapter and test adapter.
- **Bad:** `datetime.now()` hardcoded in business logic; impossible to test time-dependent behavior.
- **Good:** `Clock` interface; prod uses real time, tests inject a fixed time.

**Locality.** Related logic lives in one place. If the same concept appears twice with no shared seam, flag it.
- **Bad:** PO validation in two different microservices, both checking `quantity > 0`.
- **Good:** A shared validation seam both services call.

**Leverage.** How much capability does a caller get per unit of interface learned?
- **Bad:** `extract_invoice(pdf, model, temperature, max_tokens, retry_count, timeout)` — every caller needs to learn six parameters.
- **Good:** `extract_invoice(pdf)` with sensible defaults; callers learn one parameter.

---

## Hard Rules (Non-Negotiable)

[FINANCE-SPECIFIC — replace with actual rules from your codebase]

- **Zero framework imports in `core/` and `evals/`.** Never import `langgraph`, `langchain`, or any orchestration framework outside `orchestration/`. Enforced by CI lint check.
- **All ERP calls go through `core/tools/erp_adapter.py`.** Never call ERP APIs directly from orchestration or interfaces.
- **GL codes validated against master list.** Every coded invoice must pass `validators.gl_codes.validate(gl_code)` before ERP submission.
- **Dollar thresholds from config, never hardcoded.** Human review gates read from `core/policies/thresholds.yaml`.
- **No secrets in code.** Config reads from env vars; `.env.local` is gitignored.
- **Types for all public APIs.** Every exported function has a type signature with proper types (no `Any`).
- **Pydantic for all data crossing boundaries.** Invoice, PO, GLEntry, AuditRecord are Pydantic models in `core/models.py`.

[Add your own constraints here]

---

## Gotchas & Tribal Knowledge

[FINANCE-SPECIFIC — things that will surprise a newcomer and recur in work]

- **Example:** "`extract_invoice()` must always be called before any invoice write. Never write to invoices table directly. This creates proper cascade behavior with `invoice_line_items`."
- **Example:** "The `erp_adapter/` is generated at build time from `scripts/generate-erp-client.py` — don't edit it manually or changes will be overwritten."
- **Example:** "We cache vendor master data in Redis with a 1-hour TTL. If you change the vendor table schema, manually clear the cache or tests will fail with stale data."

[Add your own]

---

## Out-of-Scope

Before proposing a solution, check `.out-of-scope/` for ADR files explaining what has been rejected and why. Do not re-propose rejected approaches.

Example structure:
```
.out-of-scope/
  001-why-not-ocr-api.md
  002-why-no-langchain-in-core.md
  003-why-postgres-not-dynamodb.md
```

---

## Skills & Persistent Improvements

[OPTIONAL — for teams using skills extensively]

**Composable skills in use:** `/[skill-name]` — describe skills that improve this project's velocity. Example:
- `/invoice-extraction` — processes PDF invoices with consistent field mapping
- `/gl-coding` — assigns GL codes using vendor rules + ML fallback
- `/po-matching` — matches invoices to POs with fuzzy logic

**When to update a skill:** If you find yourself writing the same prompt/process twice, add it as a skill with a tool layer. Encode tribal knowledge here.

---

## What to Do When Stuck

1. **State the problem clearly:** What did you try and why didn't it work?
2. **List your options:** What are 2–3 ways forward, with tradeoffs?
3. **Ask, don't guess:** Which should we pursue — explain why one trades off against another
4. **Surface the tradeoff:** If it matters strategically, escalate to a human decision