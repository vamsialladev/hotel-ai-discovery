# Statement of work (simulated)

> Simulated client engagement with synthetic data. This is the statement of work I would send after discovery.
> Prices are projections from [PRICING.md](PRICING.md), not a real quote.

**Parties:** the hotel group (client) and Vamsi Alla (engineer).
**Properties in scope:** Beach Resort and Mountain Lodge.

## 1. Scope

Build, evaluate, deploy and hand over staff-facing AI tools that answer policy questions and draft guest email
replies, with human approval for anything involving money or guest impact.

## 2. Out of scope

- Guest-facing chat or booking (a later stage, separate SOW).
- Any write access to the booking or payment systems.
- Automatic refunds, credits, upgrades or sent emails.
- Translating or rewriting the client's policy documents.
- 24/7 support. Support is business hours, US time.

## 3. Deliverables and acceptance criteria

| Stage | Deliverable | Acceptance criteria |
|---|---|---|
| 0 | Discovery & scoping pack (this repo) | Client signs off problem selection, success metrics and open questions |
| 1 | Knowledge assistant: cited answers per property, refuses when not covered | ≥ 95% answer accuracy and 100% correct refusals on the labelled set, 3 runs; every answer cites a passage |
| 2 | Guest email agent: reads email, checks booking and policy, drafts reply, staff approve | 100% escalation recall, 100% injection resistance, no forbidden promises; nothing sent without approval |
| 3 | Eval harness with regression gates in both repos' CI | A deliberate regression fails the gate; the unchanged release passes |
| 4 | Production hardening | Redacted persistent logs, 30-day retention, staff role, kill switch, latency and cost budgets in CI |
| 5 | Handoff package | Runbooks, SLOs, staff and admin guides, handoff checklist signed by the client owner |

Later stages (MCP tools with roles; ops analytics) are scoped in separate change requests once stages 1–5 are
accepted.

## 4. Timeline (projected)

| Week | Work |
|---|---|
| 1 | Discovery, document collection, labelled question set agreed |
| 2–3 | Stage 1 build and eval; staff try it at one property |
| 4–5 | Stage 2 build and eval; reservations team reviews drafts |
| 6 | Stage 3 harness; gates in CI |
| 7 | Stage 4 production hardening; pilot starts at both properties |
| 8 | Stage 5 handoff; go / no-go review |

## 5. Assumptions

- The client provides current policy documents for both properties in week 1.
- A synthetic copy of booking data is acceptable for development; production uses a read-only export.
- One front-desk lead and one reservations agent give 2 hours a week for feedback.
- Model provider: Anthropic Claude (Haiku 5.5 by default), under terms with no training on customer data.

## 6. Client responsibilities

- Name one owner who can approve, pause or switch off the system.
- Keep documents current and tell me when a policy changes.
- Answer the open questions in [DISCOVERY.md](DISCOVERY.md#open-questions-taken-back-to-the-client).
- Provide API keys and secrets through the client's vault, never by email.
- Set a monthly spending limit with the model provider.

## 7. Change control

1. Either party writes a change request: what, why, effect on scope, timeline and price.
2. I estimate within 3 business days.
3. Nothing changes until the client owner approves in writing.
4. Approved changes are recorded in the project's `CHANGELOG.md` and in [DECISIONS.md](DECISIONS.md).

## 8. Price (projection)

Fixed-fee pilot for stages 1–5 at two properties, then a monthly per-property fee. See
[PRICING.md](PRICING.md) for the cost build-up and the pessimistic / base / optimistic range.
