# Development

```bash
git clone https://github.com/danieleongari/mol-tdn.git
cd mol-tdn
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the tests, documentation build, and package build:

```bash
pytest --cov=mol_tdn --cov-report=term-missing
mkdocs build --strict
python -m build
twine check dist/*
```

Contributions should include numerical or behavioral tests, documentation for public API changes, and citations for new equations or constants.
