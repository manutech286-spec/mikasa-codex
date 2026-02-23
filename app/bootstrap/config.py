"""Configuration loading with environment overrides."""

from __future__ import annotations

import os
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Application metadata configuration."""

    name: str
    environment: str


@dataclass(frozen=True)
class DatabaseConfig:
    """SQLite database configuration."""

    path: str


@dataclass(frozen=True)
class FeatureFlags:
    """Feature flag toggles."""

    enable_improver: bool
    enable_sync: bool
    enable_tts: bool


@dataclass(frozen=True)
class LLMConfig:
    """LLM provider configuration."""

    provider: str
    model: str
    api_key_env: str


@dataclass(frozen=True)
class UIConfig:
    """UI configuration."""

    theme: str


@dataclass(frozen=True)
class Settings:
    """Root settings object used by DI container."""

    app: AppConfig
    database: DatabaseConfig
    features: FeatureFlags
    llm: LLMConfig
    ui: UIConfig


def _env(name: str, fallback: str) -> str:
    return os.getenv(name, fallback)


def load_settings(config_path: str | Path = "config/default.toml") -> Settings:
    """Load typed settings from TOML with env var overrides."""
    with Path(config_path).open("rb") as file:
        raw = tomllib.load(file)

    return Settings(
        app=AppConfig(
            name=_env("MIKASA_APP_NAME", raw["app"]["name"]),
            environment=_env("MIKASA_ENV", raw["app"]["environment"]),
        ),
        database=DatabaseConfig(
            path=_env("MIKASA_DB_PATH", raw["database"]["path"]),
        ),
        features=FeatureFlags(
            enable_improver=_env(
                "MIKASA_FEATURE_IMPROVER",
                str(raw["features"]["enable_improver"]),
            ).lower()
            == "true",
            enable_sync=_env(
                "MIKASA_FEATURE_SYNC",
                str(raw["features"]["enable_sync"]),
            ).lower()
            == "true",
            enable_tts=_env(
                "MIKASA_FEATURE_TTS",
                str(raw["features"]["enable_tts"]),
            ).lower()
            == "true",
        ),
        llm=LLMConfig(
            provider=_env("MIKASA_LLM_PROVIDER", raw["llm"]["provider"]),
            model=_env("MIKASA_LLM_MODEL", raw["llm"]["model"]),
            api_key_env=raw["llm"]["api_key_env"],
        ),
        ui=UIConfig(theme=_env("MIKASA_UI_THEME", raw["ui"]["theme"])),
    )
