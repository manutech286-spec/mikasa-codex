"""No-op TTS adapter."""

from __future__ import annotations

from app.domain.interfaces import TTSClient


class NullTTSClient(TTSClient):
    """No-op speech adapter for offline mode."""

    def speak(self, text: str) -> None:
        """Ignore text safely."""
        _ = text
