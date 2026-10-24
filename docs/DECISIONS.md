# Decisions

Each decision: context, decision, tradeoff, result.

## 1. A discovery pack as its own repo (stage 0)

- **Context:** stages 1–5 were built and published, but the reasoning behind their order lived only in my head.
- **Decision:** write the discovery, selection, SOW, pricing and security answers as stage 0, with small tested
  scripts.
- **Tradeoff:** written after stages 1–5 were built, so it can't claim to have predicted them. The answers are
  simulated, written to match the synthetic documents.
- **Result:** every later repo can link one place for "why this, why now".

## 2. Price from measured model costs only

- **Context:** a price built on guessed token costs looks precise and isn't.
- **Decision:** the only measured inputs are cost per 1,000 requests from the release eval runs ($0.18 stage 1,
  $1.24 stage 2). Everything else is labelled an assumption.
- **Tradeoff:** the measured part is the smallest cost; the big costs (support, build) stay assumptions.
- **Result:** the pricing doc says plainly that support time, not tokens, drives the price.

## 3. Generate the pricing tables from the script

- **Context:** numbers typed into a doc drift from the code.
- **Decision:** `scripts/pricing.py --write-docs` writes the tables between markers; a test fails if the doc is out
  of date.
- **Tradeoff:** one more step when an assumption changes.
- **Result:** the doc and the script can't disagree without CI failing.

## 4. "Pessimistic" means pessimistic for the seller

- **Context:** for a business case, pessimistic means less value. For pricing, the risk is my cost going up.
- **Decision:** pessimistic = build overrun, double traffic, double support.
- **Tradeoff:** the word means different things in this pack and in the stage 1–2 business cases.
- **Result:** stated at the top of the scenario table.

## 5. Mark anything not built as Roadmap

- **Context:** a security questionnaire invites claims.
- **Decision:** every answer describes what the published stages do; SSO, region pinning and pen testing are
  marked Roadmap.
- **Tradeoff:** reads less complete than a sales answer.
- **Result:** every answer can be checked against a repo.
