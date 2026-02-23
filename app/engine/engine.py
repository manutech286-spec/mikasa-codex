"""Mikasa engine orchestration."""

from __future__ import annotations

from app.domain.interfaces import LLMClient, LLMRequest
from app.engine.event_bus import EventBus
from app.engine.events import AssistantReplyEvent, UserMessageEvent


class MikasaEngine:
    """Orchestrates command flow between UI and domain services."""

    def __init__(self, event_bus: EventBus, llm_client: LLMClient) -> None:
        self._event_bus = event_bus
        self._llm_client = llm_client

    def handle_chat(self, message: str) -> str:
        """Process chat message and publish related events."""
        self._event_bus.publish(
            UserMessageEvent(name="chat.user_message", payload={"text": message})
        )
        reply = self._llm_client.complete(LLMRequest(prompt=message))
        self._event_bus.publish(
            AssistantReplyEvent(name="chat.assistant_reply", payload={"text": reply})
        )
        return reply
