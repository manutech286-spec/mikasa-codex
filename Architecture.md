# Architecture Decisions (Iteration 1)

## Scope
This document captures safe defaults chosen for the bootable skeleton.

## Key choices
1. **Event bus is synchronous in-process** for deterministic behavior and easy testing. UI remains non-blocking because engine calls happen in presenter worker threads.
2. **SQLite path comes from TOML + env override** (`MIKASA_DB_PATH`), avoiding hardcoded paths.
3. **LLM adapter selection is config-driven** (`mock` default, `real` optional). Real adapter fails explicitly if key/env is missing.
4. **Migrations are SQL files with paired up/down scripts** and version tracking in `schema_migrations`.
5. **Rollback target semantics**: `--to VERSION` keeps VERSION and below, rolls back strictly higher versions.
6. **Theme and module widget injection points exist from day 1** (`theme.py`, `widget_registry.py`) even before full module UI is implemented.

## Pending iterations
- Memory, patients vertical slice, and improver subsystems are intentionally deferred to later iterations requested by the delivery plan.
