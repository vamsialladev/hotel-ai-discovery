# Risk register

> Simulated client engagement with synthetic data. Likelihood and impact: Low / Medium / High, my judgement at
> the end of discovery.

| # | Risk | Likelihood | Impact | Owner | Mitigation |
|---|---|---|---|---|---|
| 1 | A confident wrong answer about money or safety reaches a guest | Medium | High | Engineer | Cited answers only; numeric grounding check; refuse when not covered; safety questions skip the model and get a fixed message |
| 2 | Prompt injection in a guest email makes the agent promise a refund | Medium | High | Engineer | Email text is data; planted-instruction quarantine; model only proposes; manager approval; injection cases are 100% CI gates |
| 3 | Policy documents go out of date | High | Medium | Client (property managers) | Named document owner; index fingerprint shows when documents changed; eval re-run after updates |
| 4 | Staff stop using it (slower than asking a colleague) | Medium | High | Client (front-desk lead) + engineer | p95 latency budget in CI; first-question success measured; weekly feedback in the pilot |
| 5 | Guest personal data in logs | Medium | High | Engineer | Redact before write; 30-day retention; logs masked like a password in settings |
| 6 | Model provider outage or price change | Low | Medium | Engineer | Timeout + retry; deterministic fallback; cost per 1,000 measured every release; model swap gated by evals |
| 7 | Costs grow without anyone noticing | Low | Medium | Client (IT) | Per-session and daily caps; budgets in CI; provider spending limit set by the client |
| 8 | Credits between $51 and $200 have no named approver | High | Medium | Client (GM) | Raised in discovery; assistant says "check with a manager" for any credit over $50 until decided |
| 9 | Eval set flatters the system (written by the builder) | High | Medium | Engineer | Held-out cases written after tuning and run once; visitor questions from first-time users; outside testers next |
| 10 | LLM judge trusted before it agrees with people | Medium | Medium | Engineer | Judge calibrated against owner labels; not gated until agreement is shown (kappa 0.29 so far) |
| 11 | Free hosting sleeps and the first click fails | High | Low | Engineer | Keep-awake ping; "may take ~30 s to wake" note; always-on container for the pilot |
| 12 | Scope creep into guest-facing features | Medium | Medium | Both | SOW out-of-scope list; change control; guest-facing work needs its own SOW |
| 13 | The client can't run it after handover | Medium | High | Engineer | Runbooks, SLOs, admin guide, handoff checklist signed by the owner |
