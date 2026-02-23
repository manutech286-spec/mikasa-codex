"""Core protocol interfaces for replaceable adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    """Request payload for chat completion."""

    prompt: str
    temperature: float = 0.2


class LLMClient(Protocol):
    """LLM client abstraction."""

    def complete(self, request: LLMRequest) -> str:
        """Return response text."""


class TTSClient(Protocol):
    """TTS client abstraction."""

    def speak(self, text: str) -> None:
        """Speak provided text asynchronously or no-op."""
