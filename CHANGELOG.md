# Changelog

## Iteration 1 - Bootable Skeleton
- Created clean modular package layout under `app/` with bootstrap, engine, domain, infra, ui, tools, modules, and tests.
- Added TOML config system with environment overrides and feature flags.
- Implemented DI composition root and logging bootstrap.
- Implemented event bus and `MikasaEngine` orchestration.
- Added deterministic `MockLLMClient` and safe `RealLLMClient` stub.
- Added SQLite connection provider, migration manager, SQL migrations, and CLI tools (`migrate`, `rollback`).
- Built non-blocking PySide6 HUD skeleton with panel layout, chat flow, signals, and simple animation.
- Added tests for event bus and migration/rollback flow.
