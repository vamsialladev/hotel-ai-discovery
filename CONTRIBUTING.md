# Contributing

1. Branch from `main`; open a pull request. CI must pass.
2. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
   (`docs:`, `feat:`, `fix:`, `test:`, `ci:`).
3. Changing a pricing assumption: edit `scripts/pricing.py`, run `python scripts/pricing.py --write-docs`, commit
   both files.
4. Adding a document: add it to `REQUIRED_DOCS` in `scripts/check_docs.py` and to the README document map.
5. Keep it honest: anything not built is labelled Roadmap; every number names its source.

Run `make check` before pushing.
