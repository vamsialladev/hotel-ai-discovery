import pytest

from scripts import pricing
from scripts.pricing import Assumptions


def test_model_cost_uses_measured_cost_per_1000():
    a = Assumptions(properties=1, questions_per_property_day=1000, emails_per_property_day=0)
    assert pricing.model_cost_per_month(a) == pytest.approx(0.18 * pricing.DAYS_PER_MONTH)
    a = Assumptions(properties=1, questions_per_property_day=0, emails_per_property_day=1000)
    assert pricing.model_cost_per_month(a) == pytest.approx(1.24 * pricing.DAYS_PER_MONTH)


def test_model_cost_scales_with_properties():
    two = pricing.model_cost_per_month(Assumptions(properties=2))
    hundred = pricing.model_cost_per_month(Assumptions(properties=100))
    assert hundred == pytest.approx(two * 50)


def test_infra_and_support_grow_only_past_two_properties():
    one, two, three = (Assumptions(properties=n) for n in (1, 2, 3))
    assert pricing.infra_cost_per_month(one) == pricing.infra_cost_per_month(two)
    assert pricing.infra_cost_per_month(three) == pricing.infra_cost_per_month(two) + 5
    assert pricing.support_cost_per_month(three) == pytest.approx(pricing.support_cost_per_month(two) + 0.25 * 125)


def test_model_tokens_are_a_small_share_of_run_cost():
    # The measured token cost is cents; support time dominates. The pricing doc relies on this.
    a = Assumptions()
    assert pricing.model_cost_per_month(a) < 0.05 * pricing.run_cost_per_month(a)


def test_per_property_price_leaves_target_margin():
    a = Assumptions()
    price = pricing.per_property_month(a)
    cost_per_property = pricing.run_cost_per_month(a) / a.properties
    assert price % 10 == 0
    assert (price - cost_per_property) / price >= a.target_margin


def test_group_licence_is_discounted_against_monthly():
    a = Assumptions(properties=100)
    monthly_total = pricing.per_property_month(a) * 100 * 12
    licence = pricing.group_licence_year(a)
    assert licence % 1000 == 0
    assert licence < monthly_total
    assert licence >= monthly_total * (1 - a.group_discount)


def test_pilot_fee_covers_build_and_pilot_months():
    a = Assumptions()
    fee = pricing.pilot_fee(a)
    assert fee % 500 == 0
    assert fee >= pricing.build_cost(a) + 3 * pricing.run_cost_per_month(a)


def test_scenarios_order_costs():
    runs = {name: pricing.run_cost_per_month(pricing.scenario(name)) for name in pricing.SCENARIOS}
    assert runs["optimistic"] < runs["base"] < runs["pessimistic"]
    builds = {name: pricing.build_cost(pricing.scenario(name)) for name in pricing.SCENARIOS}
    assert builds["optimistic"] < builds["base"] < builds["pessimistic"]


def test_unknown_scenario_and_bad_inputs_raise():
    with pytest.raises(ValueError):
        pricing.scenario("wild")
    with pytest.raises(ValueError):
        pricing.per_property_month(Assumptions(target_margin=1.0))
    with pytest.raises(ValueError):
        pricing.per_property_month(Assumptions(properties=0))


def test_money_format():
    assert pricing.money(9.5) == "$9.50"
    assert pricing.money(1234.4) == "$1,234"
    assert pricing.money(80.0) == "$80"


def test_docs_are_in_sync_with_the_script():
    # docs/PRICING.md must show exactly what the script computes today.
    assert pricing.docs_block() in pricing.DOC.read_text(encoding="utf-8")


def test_write_docs_round_trip(tmp_path):
    doc = tmp_path / "PRICING.md"
    doc.write_text(f"# Pricing\n\n{pricing.START}\nold\n{pricing.END}\n\nafter\n", encoding="utf-8")
    assert pricing.write_docs(doc) is True
    assert pricing.write_docs(doc) is False
    text = doc.read_text(encoding="utf-8")
    assert "old" not in text and text.endswith("after\n")


def test_write_docs_needs_markers(tmp_path):
    doc = tmp_path / "PRICING.md"
    doc.write_text("# Pricing\n", encoding="utf-8")
    with pytest.raises(ValueError):
        pricing.write_docs(doc)


def test_cli(capsys):
    assert pricing.main(["--scenarios", "--properties", "100"]) == 0
    out = capsys.readouterr().out
    assert "Pessimistic" in out and "not results" in out
    assert pricing.main([]) == 0
    assert "per_property_month" in capsys.readouterr().out
    assert pricing.main(["--check-docs"]) == 0
