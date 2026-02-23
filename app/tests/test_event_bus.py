"""Event bus tests."""

from __future__ import annotations

from app.engine.event_bus import EventBus
from app.engine.events import Event


def test_event_bus_publish_subscribe() -> None:
    """Event handlers should receive published event payload."""
    bus = EventBus()
    seen: list[str] = []

    def handler(event: Event) -> None:
        seen.append(event.payload["text"])

    bus.subscribe("chat.user_message", handler)
    bus.publish(Event(name="chat.user_message", payload={"text": "hello"}))

    assert seen == ["hello"]
