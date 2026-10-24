"""Pricing model for the hotel-group engagement: build cost, monthly run cost and three pricing options.

Every output is a projection from the assumptions below, except the two model costs per 1,000 requests, which are
measured (release eval runs saved in vamsialladev/eval-harness, reports/p1-v1.6.0-2026-10-15.md and
reports/p2-v1.1.0-2026-10-15.md, Claude Haiku 5.5, 3 runs each).

    python scripts/pricing.py                 # base case, 2 properties
    python scripts/pricing.py --scenarios     # pessimistic / base / optimistic
    python scripts/pricing.py --properties 100 --scenarios
    python scripts/pricing.py --write-docs    # refresh the tables in docs/PRICING.md
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, replace
from pathlib import Path

DOC = Path(__file__).resolve().parent.parent / "docs" / "PRICING.md"
START, END = "<!-- pricing:start -->", "<!-- pricing:end -->"
DAYS_PER_MONTH = 30.4

# Measured: cost per 1,000 requests on the release eval runs (dev sets, 3 runs).
ASSISTANT_COST_PER_1000 = 0.18  # Knowledge Assistant v1.6.0, live keyword-only
AGENT_COST_PER_1000 = 1.24  # Guest Request Agent v1.1.0


@dataclass(frozen=True)
class Assumptions:
    properties: int = 2
    questions_per_property_day: float = 40.0  # same as the Knowledge Assistant business case
    emails_per_property_day: float = 30.0  # same as the Guest Request Agent business case
    assistant_cost_per_1000: float = ASSISTANT_COST_PER_1000
    agent_cost_per_1000: float = AGENT_COST_PER_1000
    hosting_per_month: float = 50.0  # two small always-on containers (the demo itself runs on free hosting)
    database_per_month: float = 19.0  # managed Postgres for the redacted request log
    monitoring_per_month: float = 26.0  # error tracking + uptime checks on paid starter tiers
    hosting_per_extra_property: float = 5.0  # more traffic, larger instances
    support_hours_per_month: float = 4.0  # eval re-runs, document updates, one review call
    support_hours_per_extra_property: float = 0.25
    hourly_rate: float = 125.0  # engineering rate used for build and support
    build_hours: float = 160.0  # stages 1-5 at the depth of the published repos
    pilot_months: int = 3
    target_margin: float = 0.35  # share of the per-property price left after run + support cost
    group_discount: float = 0.20  # annual group licence vs. paying per property monthly


SCENARIOS: dict[str, dict[str, float]] = {
    # Pessimistic for the seller: build overruns, more traffic, more support.
    "pessimistic": {
        "build_hours": 240.0,
        "questions_per_property_day": 80.0,
        "emails_per_property_day": 60.0,
        "support_hours_per_month": 8.0,
    },
    "base": {},
    "optimistic": {
        "build_hours": 120.0,
        "questions_per_property_day": 20.0,
        "emails_per_property_day": 15.0,
        "support_hours_per_month": 2.0,
    },
}


def scenario(name: str, base: Assumptions | None = None) -> Assumptions:
    if name not in SCENARIOS:
        raise ValueError(f"unknown scenario {name!r}; choose from {', '.join(SCENARIOS)}")
    return replace(base or Assumptions(), **SCENARIOS[name])


def model_cost_per_month(a: Assumptions) -> float:
    """Token cost per month for both apps across all properties (measured cost per request x assumed volume)."""
    per_day = (
        a.questions_per_property_day * a.assistant_cost_per_1000 + a.emails_per_property_day * a.agent_cost_per_1000
    ) / 1000
    return per_day * DAYS_PER_MONTH * a.properties


def infra_cost_per_month(a: Assumptions) -> float:
    extra = max(a.properties - 2, 0)
    return a.hosting_per_month + a.database_per_month + a.monitoring_per_month + extra * a.hosting_per_extra_property


def support_cost_per_month(a: Assumptions) -> float:
    extra = max(a.properties - 2, 0)
    return (a.support_hours_per_month + extra * a.support_hours_per_extra_property) * a.hourly_rate


def run_cost_per_month(a: Assumptions) -> float:
    return model_cost_per_month(a) + infra_cost_per_month(a) + support_cost_per_month(a)


def build_cost(a: Assumptions) -> float:
    return a.build_hours * a.hourly_rate


def round_up(value: float, step: int) -> int:
    return int(math.ceil(value / step) * step)


def pilot_fee(a: Assumptions) -> int:
    """Fixed-fee pilot: the build plus run and support for the pilot months, rounded up to $500."""
    return round_up(build_cost(a) + a.pilot_months * run_cost_per_month(a), 500)


def per_property_month(a: Assumptions) -> int:
    """Monthly price per property that leaves the target margin after run and support cost, rounded up to $10."""
    if not 0 <= a.target_margin < 1:
        raise ValueError("target_margin must be in [0, 1)")
    if a.properties < 1:
        raise ValueError("properties must be at least 1")
    return round_up(run_cost_per_month(a) / a.properties / (1 - a.target_margin), 10)


def group_licence_year(a: Assumptions) -> int:
    """Annual licence for the whole group: 12 months of the per-property price, discounted, rounded up to $1,000."""
    return round_up(per_property_month(a) * a.properties * 12 * (1 - a.group_discount), 1000)


def summary(a: Assumptions) -> dict[str, float]:
    return {
        "model": model_cost_per_month(a),
        "infra": infra_cost_per_month(a),
        "support": support_cost_per_month(a),
        "run": run_cost_per_month(a),
        "build": build_cost(a),
        "pilot": pilot_fee(a),
        "per_property_month": per_property_month(a),
        "group_year": group_licence_year(a),
    }


def money(value: float) -> str:
    if value < 100 and value != int(value):
        return f"${value:,.2f}"
    return f"${value:,.0f}"


def table(properties: int) -> str:
    rows = [
        "| | Pessimistic | Base | Optimistic |",
        "|---|---|---|---|",
    ]
    results = {name: summary(scenario(name, Assumptions(properties=properties))) for name in SCENARIOS}
    labels = [
        ("model", "Model tokens per month (measured cost x assumed volume)"),
        ("infra", "Hosting, database, monitoring per month"),
        ("support", "Support per month"),
        ("run", "**Run cost per month**"),
        ("build", "Build cost (one time)"),
        ("pilot", "**Fixed-fee pilot** (build + 3 months at this size)"),
        ("per_property_month", "**Per property per month**"),
        ("group_year", "**Group licence per year**"),
    ]
    for key, label in labels:
        rows.append(f"| {label} | " + " | ".join(money(results[n][key]) for n in SCENARIOS) + " |")
    return "\n".join(rows)


def docs_block() -> str:
    parts = [START, "", "_Generated by `python scripts/pricing.py --write-docs`. Projections, not results._", ""]
    for properties in (2, 100):
        parts += [f"### {properties} properties", "", table(properties), ""]
    parts.append(END)
    return "\n".join(parts)


def write_docs(path: Path = DOC) -> bool:
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise ValueError(f"{path} has no {START} ... {END} block")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = head + docs_block() + tail
    changed = new != text
    if changed:
        path.write_text(new, encoding="utf-8", newline="\n")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--properties", type=int, default=2)
    parser.add_argument("--scenarios", action="store_true", help="show pessimistic / base / optimistic")
    parser.add_argument("--write-docs", action="store_true", help="refresh the generated tables in docs/PRICING.md")
    parser.add_argument("--check-docs", action="store_true", help="fail if docs/PRICING.md is out of date")
    args = parser.parse_args(argv)
    if args.check_docs:
        text = DOC.read_text(encoding="utf-8")
        if docs_block() not in text:
            print("docs/PRICING.md is out of date: run python scripts/pricing.py --write-docs")
            return 1
        print("docs/PRICING.md is up to date")
        return 0
    if args.write_docs:
        print("updated docs/PRICING.md" if write_docs() else "docs/PRICING.md already up to date")
        return 0
    print(f"Projections for {args.properties} properties (not results).\n")
    if args.scenarios:
        print(table(args.properties))
    else:
        for key, value in summary(Assumptions(properties=args.properties)).items():
            print(f"{key:>20}: {money(value)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
