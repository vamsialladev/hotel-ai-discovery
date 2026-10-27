# Video script: Discovery & Scoping pack (75 seconds)

Recorded by me, in my own voice, on a screen recording of this repo on github.com. Until I do, the AI-narrated version is in `docs/video/demo-ai-voice.mp4` (narration at the end of this file). Setup and tips:
`RECORDING_GUIDE.md` in my portfolio folder. Read it twice, then talk from the bullets. `/` marks a natural pause.

There's no live app for this stage, so the "action" shots show the documents and the pricing script running.

## Shot list

| Time | On screen | What I say (spoken, natural) |
|---|---|---|
| 0–10 s | README, first screen | Before I wrote any code for this hotel group, / I spent a day just asking questions. / This repo is what came out of that. It's a simulated client, with synthetic data. |
| 10–30 s | `docs/DISCOVERY.md`, scroll to the front-desk lead table | I talked to six people. / The GM, the front-desk lead, activities, revenue, IT, and a guest. / The front-desk lead told me a guest waited four minutes while they radioed a manager about one fee. / That one answer shaped stage one. |
| 30–45 s | `docs/PROBLEM_SELECTION.md`, the 4-check table | I scored six ideas, / then ran a four-check test. / Has someone felt it, would someone pay, can I build a first version in a week, do I know the first user. / Automatic refunds failed. / The GM said that's exactly what would make them switch it off. |
| 45–60 s | Terminal: `python scripts/pricing.py --scenarios` | Here's pricing. / The only measured input is the model cost, / eighteen cents per thousand questions, and a dollar twenty-four per thousand emails. / Everything else is an assumption, / so it's a range, not a promise. |
| 60–75 s | `docs/INTERVIEW_WALKTHROUGH.md`, then the stage table in the README | The point is the order. / Staff-facing before guests, read-only before anything that writes. / Every stage after this one links back here. / The links are in the README. |

## Exact inputs (tested)

```bash
python scripts/pricing.py --scenarios
```

Tested 2026-10-24 on Windows, Python 3.12: prints the pessimistic / base / optimistic table for 2 properties.

## LinkedIn caption (one sentence)

Before writing code for a (simulated) hotel group, I ran discovery with six stakeholders, scored six ideas with a
four-check test, and priced it from measured model costs: here's the pack.

## AI narration (used in docs/video/demo-ai-voice.mp4)

Until I record my own voice, the demo video (1:20) is narrated by an AI voice (Kokoro `af_heart`, local) and labelled "AI-narrated" on screen and here. It was recorded from the rendered documents on GitHub with Playwright; the captions are the narration, timed to the voice. `/` marks a pause.

| Step | Narration |
|---|---|
| problem | Before I wrote any code for this hotel group, / I spent a day just asking questions. / This repo is what came out of that. / It's a simulated client, with synthetic data. |
| discovery | I talked to six people. / The general manager, the front-desk lead, activities, revenue, IT, and a guest. / The front-desk lead told me a guest waited four minutes while they radioed a manager about one fee. / That one answer shaped the first stage. |
| selection | I scored six ideas, / then ran a four-check test. / Has someone felt it, would someone pay, can I build a first version in a week, and do I know the first user. / Automatic refunds failed. / The manager said that's exactly what would make them switch it off. |
| pricing | Here's the pricing. / The only measured input is the model cost: / eighteen cents per thousand questions, and about a dollar twenty-four per thousand emails. / Everything else is an assumption, / so it's a range, not a promise. |
| order | The point is the order. / Staff-facing before guests, / read-only before anything that writes. / Every later stage links back here, and the links are in the README. |
