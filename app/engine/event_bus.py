"""In-process event bus implementation."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from app.engine.events import Event

EventHandler = Callable[[Event], None]


class EventBus:
    """Simple synchronous publish/subscribe bus."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Register handler for event name."""
        self._handlers[event_name].append(handler)

    def publish(self, event: Event) -> None:
        """Publish event to all handlers."""
        for handler in self._handlers.get(event.name, []):
            handler(event)
