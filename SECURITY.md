# Security

## Reporting a vulnerability

Email <vamsialla.dev@gmail.com> with steps to reproduce. Please don't open a public issue for a security problem.

## This repo

Documents and two scripts that read no secrets, call no API and touch no personal data. gitleaks runs in
pre-commit and CI; `.env` is git- and Docker-ignored.

## Threat model (the proposed system)

| Asset | Threat | Mitigation | Where it's built |
|---|---|---|---|
| Guest personal data | Leaks into logs or the model | Redact before writing; send only needed fields | Stage 4 (`src/pii.py` in both apps) |
| Money decisions | Agent promises a refund or upgrade | Model only proposes; manager approval; no-promise check is a CI gate | Stage 2 |
| Agent behaviour | Prompt injection through an email or document | Text is data; planted-instruction quarantine; injection gates at 100% | Stages 2, 4 |
| Bookings | One guest reads another's booking | Sender-scoped lookup; roles in the tool server | Stages 2, 7 |
| Budget | Cost spike from abuse | Session and daily caps; budgets in CI; provider limit | Stages 1, 4 |
| Availability | Outage unnoticed | Daily health check opens an issue | Stage 5 |
| Secrets | Key committed or logged | Secrets store only; masked in records; secret scanning + gitleaks | All stages |

## OWASP Top 10 for LLM applications (2025)

| # | Risk | How the proposed system handles it |
|---|---|---|
| LLM01 | Prompt injection | Email and document text treated as data; planted instructions quarantined; injection cases are hard gates |
| LLM02 | Sensitive information disclosure | Redaction before logging; minimal context to the model; sender-scoped booking lookup |
| LLM03 | Supply chain | Pinned dependencies, pip-audit, Dependabot, secret scanning |
| LLM04 | Data and model poisoning | Documents edited only by named owners; index fingerprint; eval re-run after document changes |
| LLM05 | Improper output handling | Answers escaped before display; tool inputs validated with typed schemas; no model output executed |
| LLM06 | Excessive agency | Tools are read-only or "propose" only; anything with money or guest impact needs a person |
| LLM07 | System prompt leakage | No secrets in prompts; prompts assumed public |
| LLM08 | Vector and embedding weaknesses | Property filter on retrieval; tenant ID on every record in the tool server |
| LLM09 | Misinformation | Citations required; numeric grounding check; refuse when not covered |
| LLM10 | Unbounded consumption | Per-session and daily caps, timeouts, budgets in CI, provider spending limit |
