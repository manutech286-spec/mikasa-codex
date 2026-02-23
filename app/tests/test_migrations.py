"""Migration manager tests."""

from __future__ import annotations

from pathlib import Path

from app.infra.db.migration_manager import MigrationManager
from app.infra.db.sqlite_db import SQLiteDatabase


def test_migrate_and_rollback(tmp_path: Path) -> None:
    """Migration manager should apply and rollback versions deterministically."""
    db_file = tmp_path / "test.db"
    db = SQLiteDatabase(str(db_file))
    conn = db.connect()
    manager = MigrationManager(conn, "app/infra/db/migrations")

    applied = manager.migrate()

    assert applied == ["001", "002"]
    tables = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    assert "app_events" in tables
    assert "user_preferences" in tables

    rolled_back = manager.rollback_to("001")

    assert rolled_back == ["002"]
    tables_after = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    assert "user_preferences" not in tables_after
