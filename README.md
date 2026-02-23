# MIKASA CODEX (Lab)

Parallel lab project for a production-grade, modular desktop veterinary assistant core.

## Stack
- Python 3.11
- PySide6 desktop UI
- SQLite persistence
- Pytest

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m app.tools.migrate
python -m app.main
```

## Rollback migrations
```bash
python -m app.tools.rollback --to 001
```

## Tests
```bash
pytest
```
