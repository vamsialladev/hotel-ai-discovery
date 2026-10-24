from scripts import check_docs


def test_pack_has_no_problems():
    assert check_docs.problems() == []


def test_placeholder_shapes():
    assert check_docs.placeholders("link YOUR-STREAMLIT-APP here") == ["YOUR-STREAMLIT-APP"]
    assert check_docs.placeholders("see https://example.com") == ["example.com"]
    assert check_docs.placeholders("a TODO item") == ["TODO"]
    assert check_docs.placeholders("your team and today") == []


def test_local_links_skip_urls():
    text = "[a](docs/SOW.md) [b](https://x.org) [c](RISKS.md#owner) [d](mailto:a@b.c)"
    assert check_docs.local_links(text) == ["docs/SOW.md", "RISKS.md"]


def test_problems_reports_missing_and_broken(tmp_path):
    (tmp_path / "README.md").write_text("[gone](docs/NOPE.md) YOUR-EMAIL", encoding="utf-8")
    found = check_docs.problems(tmp_path)
    assert "missing docs/SOW.md" in found
    assert "README does not link docs/SOW.md" in found
    assert "README.md: broken link docs/NOPE.md" in found
    assert "README.md: placeholder 'YOUR-EMAIL'" in found
