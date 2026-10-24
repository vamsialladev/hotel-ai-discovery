# Problem selection

> Simulated client engagement with synthetic data. Scores are my judgement after the discovery session, not
> measurements.

Six candidate use cases came out of discovery. I scored each from 1 (poor) to 5 (strong) on four things, then ran
a 4-check test before committing to build anything.

## Scores

| # | Use case | Value | Feasibility | Risk (5 = low) | Data readiness | Total |
|---|---|---|---|---|---|---|
| A | Policy knowledge assistant for front-desk staff | 4 | 5 | 4 | 4 | **17** |
| B | Guest email agent: drafts replies, staff approve | 5 | 4 | 3 | 4 | **16** |
| C | Guest activities concierge (QR code in the room) | 4 | 3 | 3 | 2 | **12** |
| D | Hotel tools for any AI client, with roles and audit (MCP) | 3 | 4 | 4 | 3 | **14** |
| E | Revenue questions in plain English + daily anomaly alert | 4 | 3 | 3 | 3 | **13** |
| F | Automatic refunds and upgrades decided by AI | 3 | 3 | 1 | 2 | **9** |

### Why the scores

- **A** Every shift feels it; documents exist; read-only; the worst case is a wrong answer a person sees first.
- **B** Highest value (30 emails a day at 6–8 minutes each) but higher risk: an email can carry an injected
  instruction, and a reply can promise money. Needs approval and an eval of its own.
- **C** Guests want it, but the activity data is a printed spreadsheet and it's guest-facing. Needs clean data and
  staff trust first.
- **D** Low direct value alone, but it makes every later tool safer: one place for roles, limits and audit.
- **E** Clear value for one person. Data is messy and a wrong number in a board pack is costly, so the SQL must be
  shown and checked.
- **F** Rejected. It removes the human from money decisions, which the GM named as the reason to switch it off.

## The 4-check test

| # | Use case | Someone has felt the problem | Someone would pay | V1 buildable in a week | First customer known | Pass? |
|---|---|---|---|---|---|---|
| A | Knowledge assistant | Yes: front-desk lead, 4-minute radio call | Yes: GM owns the pilot budget | Yes | Yes: Mountain Lodge front desk | **Pass** |
| B | Guest email agent | Yes: 6–8 min per email, promises made to calm guests | Yes: same budget | Yes, reusing A for policy | Yes: reservations team | **Pass** |
| C | Activities concierge | Yes: walk-ups turned away | Probably: activities budget, not confirmed | No: activity data needs cleaning first | Not yet: no property has agreed to a guest pilot | **Not yet** |
| D | MCP tools + RBAC | Yes: IT's worry about tricked AI | Indirectly: needed for roll-out | Yes | Yes: IT/security | **Pass (as an enabler)** |
| E | Ops analytics | Yes: half a day per custom question; a rate error missed for a week | Yes: revenue manager | Yes, on a synthetic copy | Yes: revenue manager | **Pass** |
| F | Automatic refunds | Yes | No: GM would switch it off | Technically | No | **Fail** |

## The order, and why

| Stage | What | Why it comes here |
|---|---|---|
| 0 | Discovery & scoping (this pack) | Agree the problem, the data and what "working" means before writing code. |
| 1 | Knowledge assistant (A) | Lowest risk, highest feasibility. Builds the retrieval and citation layer everything else reuses. |
| 2 | Guest email agent (B) | Highest value, but only safe once policy answers are trusted. Uses stage 1 as a tool. |
| 3 | Eval harness | Two LLM features now exist. One harness with regression gates stops a fix in one from breaking the other. |
| 4 | Production | Fixes found by the evals, redacted persistent logs, staff role, budgets, kill switch, monitoring. |
| 5 | Handoff | Runbooks, SLOs and guides so the client can own it without me. |
| 6 | Activities concierge (C) | First guest-facing system. Waits until the data is clean and staff trust the staff-facing tools. Not built yet. |
| 7 | MCP tools + RBAC (D) | Before more tools and clients connect, put roles, limits and audit in one place. |
| 8 | Ops analytics (E) | Read-only data access is safer once roles and audit exist (stage 7). |

Two rules decided the order: **staff-facing before guest-facing**, and **read-only before anything that writes**.
Evals come before production because "it worked in the demo" isn't evidence.
