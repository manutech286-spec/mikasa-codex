"""SQLite connection factory."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteDatabase:
    """Lightweight SQLite connection provider."""

    def __init__(self, db_path: str) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """Create configured SQLite connection."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn
