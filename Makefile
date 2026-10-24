.PHONY: check test lint docs pricing

check: lint test docs

lint:
	ruff check .
	ruff format --check .

test:
	python -m pytest

docs:
	python scripts/check_docs.py
	python scripts/pricing.py --check-docs

pricing:
	python scripts/pricing.py --scenarios
