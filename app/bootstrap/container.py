"""Composition root / dependency injection container."""

from __future__ import annotations

from dataclasses import dataclass

from app.bootstrap.config import Settings, load_settings
from app.bootstrap.logging_config import configure_logging
from app.engine.engine import MikasaEngine
from app.engine.event_bus import EventBus
from app.infra.db.migration_manager import MigrationManager
from app.infra.db.sqlite_db import SQLiteDatabase
from app.infra.llm.mock_client import MockLLMClient
from app.infra.llm.real_client import RealLLMClient
from app.infra.tts.null_tts import NullTTSClient


@dataclass
class Container:
    """Top-level object graph holder."""

    settings: Settings
    event_bus: EventBus
    engine: MikasaEngine
    tts: NullTTSClient
    db: SQLiteDatabase
    migration_manager: MigrationManager


def build_container(config_path: str = "config/default.toml") -> Container:
    """Create application container with configured dependencies."""
    configure_logging()
    settings = load_settings(config_path)

    event_bus = EventBus()
    db = SQLiteDatabase(settings.database.path)
    conn = db.connect()
    migration_manager = MigrationManager(conn, "app/infra/db/migrations")
    migration_manager.ensure_table()

    if settings.llm.provider == "real":
        llm_client = RealLLMClient(settings.llm.model, settings.llm.api_key_env)
    else:
        llm_client = MockLLMClient(seed=42)

    engine = MikasaEngine(event_bus=event_bus, llm_client=llm_client)
    return Container(
        settings=settings,
        event_bus=event_bus,
        engine=engine,
        tts=NullTTSClient(),
        db=db,
        migration_manager=migration_manager,
    )
