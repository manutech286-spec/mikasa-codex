"""SQLite migration and rollback management."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class MigrationManager:
    """Apply and rollback SQL migrations."""

    def __init__(self, conn: sqlite3.Connection, migrations_dir: str | Path) -> None:
        self._conn = conn
        self._migrations_dir = Path(migrations_dir)

    def ensure_table(self) -> None:
        """Ensure migration tracking table exists."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def applied_versions(self) -> set[str]:
        """Return set of applied versions."""
        rows = self._conn.execute("SELECT version FROM schema_migrations").fetchall()
        return {row[0] for row in rows}

    def migrate(self) -> list[str]:
        """Apply pending up migrations in version order."""
        self.ensure_table()
        applied = self.applied_versions()
        ran: list[str] = []
        for up_file in sorted(self._migrations_dir.glob("*_up.sql")):
            version = up_file.name.split("_")[0]
            if version in applied:
                continue
            sql = up_file.read_text(encoding="utf-8")
            self._conn.executescript(sql)
            self._conn.execute(
                "INSERT INTO schema_migrations(version, applied_at) VALUES(?, datetime('now'))",
                (version,),
            )
            self._conn.commit()
            ran.append(version)
        return ran

    def rollback_to(self, target_version: str) -> list[str]:
        """Rollback applied migrations until target version is top-most applied."""
        self.ensure_table()
        versions = sorted(self.applied_versions(), reverse=True)
        rolled_back: list[str] = []
        for version in versions:
            if version <= target_version:
                continue
            down_file = next(self._migrations_dir.glob(f"{version}_*_down.sql"), None)
            if down_file is None:
                raise FileNotFoundError(f"Missing down migration for version {version}")
            self._conn.executescript(down_file.read_text(encoding="utf-8"))
            self._conn.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
            self._conn.commit()
            rolled_back.append(version)
        return rolled_back
