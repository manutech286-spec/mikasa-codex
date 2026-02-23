"""Migration CLI."""

from __future__ import annotations

from app.bootstrap.config import load_settings
from app.infra.db.migration_manager import MigrationManager
from app.infra.db.sqlite_db import SQLiteDatabase


def main() -> int:
    """Run pending migrations."""
    settings = load_settings()
    db = SQLiteDatabase(settings.database.path)
    conn = db.connect()
    manager = MigrationManager(conn, "app/infra/db/migrations")
    versions = manager.migrate()
    print(f"Applied migrations: {versions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
