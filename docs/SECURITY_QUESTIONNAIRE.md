# Security questionnaire (simulated)

> Simulated client engagement with synthetic data. Answers describe what the published stages actually do;
> anything not built is marked **Roadmap**. A real questionnaire would be answered for the client's chosen
> hosting and signed off by their security team.

| # | Question | Answer |
|---|---|---|
| 1 | **Data residency.** Where is customer data stored and processed? | Request logs in a managed Postgres in a US region. The model provider processes prompts in the US. Policy documents live in the app's repo and container. Region pinning for a client's own cloud is **Roadmap**. |
| 2 | **Retention.** How long is data kept? | Request logs 30 days, deleted by a daily retention job. Feedback is linked to requests and follows the same rule. The model provider's retention follows its API terms. |
| 3 | **Encryption.** In transit and at rest? | TLS for every connection (browser, model API, database). Database encryption at rest is provided by the managed host. |
| 4 | **SSO.** Do you support single sign-on? | Not in the pilot: staff and admin roles use separate passwords from the secrets store, with a 30-minute auto-lock on Admin. OIDC/SSO is designed and documented as the next step (**Roadmap**). |
| 5 | **RBAC.** Can access be limited by role? | Yes: guest-demo, staff and owner/admin roles in the apps. A tool server with guest, front desk, manager and auditor roles is stage 7. |
| 6 | **Audit logs.** Is every action recorded? | Every request is logged with request ID, anonymous session ID, outcome, citations, tokens, cost and timing, redacted before writing. The tool server writes an append-only audit log with role, tool, argument hash and status. |
| 7 | **Subprocessors.** Who else handles our data? | Anthropic (model API), the database host, the app host. Code hosting and CI on GitHub see no customer data (tests use synthetic data). |
| 8 | **Model training on customer data.** | No. The model is used through the commercial API, whose terms exclude training on API inputs by default. No fine-tuning on client data. |
| 9 | **What data is sent to the model?** | Only what the answer needs: the question and retrieved passages; for emails, the email and the booking fields used. Never raw history or full guest profiles. |
| 10 | **PII handling.** | Names, emails, phones and card numbers are redacted and booking IDs hashed before any log write. Secret values and API-key shapes are masked in every record. |
| 11 | **Incident response.** | The owner can switch the AI off with one setting (kill switch). I notify the client owner within 24 hours with what happened, data involved and the fix. Runbooks cover outage, cost spike, bad answer and suspected injection. |
| 12 | **Penetration testing.** | Not performed for the pilot. Prompt-injection and must-refuse cases run as hard CI gates on every change. A third-party pen test before any guest-facing launch is **Roadmap**. |
| 13 | **Vulnerability management.** | `pip-audit` in CI, Dependabot updates, pinned dependencies, secret scanning with push protection on every repo, gitleaks in pre-commit and CI. |
| 14 | **Secrets.** | Only in the host's secrets store or a local `.env` that git and Docker ignore. Never in code, logs or email. |
| 15 | **Prompt injection.** | Email and document text are treated as data. Planted instructions are quarantined; the model can only propose actions; money and guest-impact actions need manager approval. |
| 16 | **Availability.** | Business-hours support for the pilot. Daily health check opens an issue when an app is down. SLOs are written in the handoff package. |
| 17 | **Data deletion on exit.** | On request: drop the client's log tables, delete secrets, remove the deployment. Documents are returned. |
| 18 | **Change management.** | Every change on a branch with a PR, CI (lint, tests, coverage, eval gates) must pass before merge. |
