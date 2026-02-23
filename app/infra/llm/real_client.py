"""Real LLM adapter stub behind interface."""

from __future__ import annotations

import os

from app.domain.interfaces import LLMClient, LLMRequest


class RealLLMClient(LLMClient):
    """Production adapter placeholder with explicit failure mode."""

    def __init__(self, model: str, api_key_env: str) -> None:
        self._model = model
        self._api_key_env = api_key_env

    def complete(self, request: LLMRequest) -> str:
        """Call external provider when implemented."""
        api_key = os.getenv(self._api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing API key in env var '{self._api_key_env}' for model '{self._model}'."
            )
        raise NotImplementedError("RealLLMClient integration is not implemented yet.")
