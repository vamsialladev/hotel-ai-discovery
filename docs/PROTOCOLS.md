# Agent protocols for this engagement

Which agent protocol each part of the hotel system uses, why, and where the working examples are. The examples
live in [agent-protocols-lab](https://github.com/vamsialladev/agent-protocols-lab): one small, tested demo per
protocol in the same hotel scenario (simulated client, synthetic data).

## What the hotel system uses

| Connection | Protocol | Status in the build |
|---|---|---|
| Any app → the hotel group's tools and policy (stage 7) | MCP | Built: the concierge (guest role) and Ops Analytics (manager role, `search_policy` only) |
| Concierge (stage 6) → Guest Request Agent (stage 2) | A2A | Built: agent card, bearer token, task lifecycle; falls back to the front desk when the agent can't be reached |
| Concierge run → its page | AG-UI events | Built: every answer is stored as AG-UI events and the step timeline is drawn from them |
| Paid activities | AP2 (sandbox) | Built: mandates with a guest approval and a daily limit; no real money |

## How I'd choose for a new connection

| If the need is... | Use | Not |
|---|---|---|
| An agent calling tools or reading data | MCP | A2A (that's for agents you don't own) |
| Handing a task to another team's or vendor's agent | A2A | ACP (merged into A2A in 2025) |
| Agents from different owners finding and trusting each other | ANP | A shared bearer token |
| Streaming a run, with approvals, to a front end | AG-UI | A custom WebSocket format |
| An agent returning UI inside the hotel's design system | A2UI, with an allowlisted renderer | Agent-written HTML |
| An agent paying on a guest's behalf | AP2, with the guest's approval | Letting the agent hold payment credentials |
| An agent buying from many merchants | UCP | One-off merchant integrations |
| Per-call paid APIs | x402 | Card payments for cents |

Each row's demo, status checks and security notes: the lab's
[protocol reference](https://github.com/vamsialladev/agent-protocols-lab#protocol-reference).

## What I'd check before adopting any of them

1. The current spec version and whether it has merged or been renamed (ACP did).
2. Whether the official SDK installs next to the client's other dependencies (AP2's pins exact versions).
3. Whether the PyPI or npm name is the real project (the PyPI `ap2` isn't).
4. The guardrail it needs on day one: allowlists, signatures, replay protection, spending limits, a human approval.
