"""Rollback CLI."""

from __future__ import annotations

import argparse

from app.bootstrap.config import load_settings
from app.infra.db.migration_manager import MigrationManager
from app.infra.db.sqlite_db import SQLiteDatabase


def main() -> int:
    """Rollback migrations to target version."""
    parser = argparse.ArgumentParser(description="Rollback SQLite schema")
    parser.add_argument("--to", required=True, help="Target version to keep")
    args = parser.parse_args()

    settings = load_settings()
    db = SQLiteDatabase(settings.database.path)
    conn = db.connect()
    manager = MigrationManager(conn, "app/infra/db/migrations")
    versions = manager.rollback_to(args.to)
    print(f"Rolled back versions: {versions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
