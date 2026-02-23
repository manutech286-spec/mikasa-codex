"""Event contracts for internal pub/sub."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Event:
    """Base application event."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    ts: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class UserMessageEvent(Event):
    """Message submitted by user."""


@dataclass(frozen=True)
class AssistantReplyEvent(Event):
    """Reply returned by assistant."""
