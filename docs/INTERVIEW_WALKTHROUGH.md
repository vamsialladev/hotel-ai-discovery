# Interview walkthrough: a 60-minute FDE system-design round

> How I'd present this simulated engagement in a design interview. The numbers quoted are from the saved eval
> reports in each stage's repo; the client is fictional and the data synthetic.

## 0–15 min: discovery questions (out loud, before any boxes)

I start by asking, not drawing. The questions I'd ask the interviewer-as-client:

1. Who uses it: staff or guests? (Staff first changes the risk.)
2. What does a wrong answer cost? Who gets blamed?
3. Which actions involve money or guest impact? Who approves them today?
4. Where do the facts live, and who keeps them current?
5. What data is personal, and where must it stay?
6. How many requests a day, and when are the peaks?
7. What does "working" look like in three months? How would we measure it?
8. What would make you switch it off?
9. How do people sign in today? Is there SSO?
10. What languages do guests write in?

Then I play back: users, success metrics, data and sensitivity, constraints, open questions. (Same headings as
[DISCOVERY.md](DISCOVERY.md).)

## 15–45 min: design

1. **Pick the first problem** with the scores and the 4-check test ([PROBLEM_SELECTION.md](PROBLEM_SELECTION.md)).
   Staff-facing before guest-facing; read-only before anything that writes.
2. **Draw the flow** for one request ([ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md)): retrieve with a
   property filter → answer with citations → check grounding → log after redaction.
3. **Add the agent:** booking lookup by sender before the model, tools with typed inputs, the model only
   proposes, approvals for money.
4. **Say how I'd know it works:** labelled eval set with must-refuse and injection cases, held-out set run once,
   3 runs, cost per 1,000, p95, CI gate.
5. **Price it** ([PRICING.md](PRICING.md)): measured token cost is tiny; support time drives the price.

## The 5 "Design at scale" points

| Point | What I'd say |
|---|---|
| Model choice | Haiku 5.5 by default: in stage 1 it matched Haiku 4.5 within run-to-run range (97% vs. 98%) at about a fifth of the cost. Any change goes through the eval harness. |
| PII and tenant isolation | Send the model only what it needs; redact before writing; property as a filter; `hotel_group_id` on every record with tests that prove no cross-tenant reads. |
| 10K → 1M | First break: free hosting sleeps, then the per-app index, then the shared budget, then model rate limits at peaks. Fixes: always-on, index built in CI, per-property budgets, queue + caching + second region. |
| Monitoring and hallucinations | Grounding check on every answer; request log with cost and latency; daily health check; eval gates on every change. LLM judge only once it agrees with people. |
| Failure modes and rollback | Timeout + retry + deterministic fallback; kill switch; redeploy previous tag; budgets and caps. |

## 45–60 min: likely follow-ups

| Question | Short answer |
|---|---|
| Why not fine-tune? | Policies change weekly. Retrieval updates with a re-index; fine-tuning would need a re-train and still hallucinate stale facts. |
| How do you stop prompt injection? | Treat email and document text as data, quarantine planted instructions, let the model only propose, gate on injection cases. Stage 2 resisted 100% of its injection cases; one held-out case (H03) had failed before a fix. |
| How do you know the eval isn't flattering you? | I wrote it, so it does. Held-out cases written last and run once; testing like a first-time visitor showed 43% first-question success while my own eval said 96–98%. |
| What if the judge model is wrong? | It was: kappa 0.29 against my labels. Nothing is gated on it. Deterministic checks first. |
| Hybrid search or keyword? | Keyword-only was enough for most questions; hybrid helped only meaning-only questions. Measured both: 98% vs. 97% answer accuracy. |
| How do you hand it over? | Runbooks, SLOs, staff and admin guides, a checklist the client owner signs, a daily health check. |
| What does it cost to run? | Measured $0.18 per 1,000 questions (stage 1) and $1.24 per 1,000 emails (stage 2). |
| What would you do differently? | Test like a first-time visitor on day one, not after the eval says 96%. |
