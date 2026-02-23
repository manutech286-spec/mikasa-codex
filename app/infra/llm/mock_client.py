"""Deterministic mock LLM adapter for tests and local runs."""

from __future__ import annotations

import random

from app.domain.interfaces import LLMClient, LLMRequest


class MockLLMClient(LLMClient):
    """Seeded mock client that returns deterministic outputs."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)

    def complete(self, request: LLMRequest) -> str:
        """Return deterministic pseudo-natural reply."""
        suffix = self._rng.choice(["Understood.", "Got it.", "I can help with that."])
        return f"Mikasa: {request.prompt.strip()} — {suffix}"
