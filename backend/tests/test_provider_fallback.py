import asyncio

import pytest

from app.ai.providers.base import ProviderError
from app.ai.ai_manager import AIManager


class FakeProvider:
    def __init__(self, errors_before_success=0):
        self.calls = []
        self.errors_before_success = errors_before_success

    async def chat(self, messages, *, model, temperature=0.7, response_format=None):
        self.calls.append(model)
        if self.errors_before_success > 0:
            self.errors_before_success -= 1
            raise ProviderError("temporarily overloaded", retryable=True)
        return "ok"


@pytest.mark.asyncio
async def test_retry_then_success(monkeypatch):
    manager = AIManager()
    fake = FakeProvider(errors_before_success=2)
    monkeypatch.setattr(manager, "provider_for", lambda role: (fake, {
        "provider": "openrouter",
        "api_key": "key",
        "base_url": "https://openrouter.ai/api/v1",
        "model": "primary",
        "fallback_models": ["fallback"],
        "temperature": 0.2,
    }))
    monkeypatch.setattr("app.ai.ai_manager.settings.ai_retry_count", 2)
    monkeypatch.setattr("app.ai.ai_manager.settings.ai_retry_delay_seconds", 0)
    result = await manager.chat("judge", [{"role": "user", "content": "x"}])
    assert result == "ok"
    assert fake.calls == ["primary", "primary", "primary"]


@pytest.mark.asyncio
async def test_fallback_model_after_primary_exhausted(monkeypatch):
    manager = AIManager()

    class FailingPrimaryThenFallback(FakeProvider):
        async def chat(self, messages, *, model, temperature=0.7, response_format=None):
            self.calls.append(model)
            if model == "primary":
                raise ProviderError("overloaded", retryable=True)
            return "fallback-ok"

    fake = FailingPrimaryThenFallback()
    monkeypatch.setattr(manager, "provider_for", lambda role: (fake, {
        "provider": "openrouter",
        "api_key": "key",
        "base_url": "https://openrouter.ai/api/v1",
        "model": "primary",
        "fallback_models": ["fallback"],
        "temperature": 0.2,
    }))
    monkeypatch.setattr("app.ai.ai_manager.settings.ai_retry_count", 1)
    monkeypatch.setattr("app.ai.ai_manager.settings.ai_retry_delay_seconds", 0)
    result = await manager.chat("judge", [{"role": "user", "content": "x"}])
    assert result == "fallback-ok"
    assert fake.calls == ["primary", "primary", "fallback"]
