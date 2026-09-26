import asyncio
from app.ai.providers.base import ProviderError, LLMProvider
from app.ai.providers.openai_compatible import OpenAICompatibleProvider
from app.ai.providers.gemini import GeminiProvider
from app.config.settings import settings

class AIManager:
    PROVIDERS = {
        "openai": OpenAICompatibleProvider,
        "openai_compatible": OpenAICompatibleProvider,
        "openrouter": OpenAICompatibleProvider,
        "groq": OpenAICompatibleProvider,
        "together": OpenAICompatibleProvider,
        "deepseek": OpenAICompatibleProvider,
        "xai": OpenAICompatibleProvider,
        "mistral": OpenAICompatibleProvider,
        "gemini": GeminiProvider,
    }

    def provider_for(self, role: str) -> tuple[LLMProvider, dict]:
        config = settings.role_ai_config(role)
        provider_cls = self.PROVIDERS.get(config["provider"].lower().strip())
        if not provider_cls:
            raise ProviderError(f"Unsupported {role} AI provider '{config['provider']}'.")
        provider = provider_cls(api_key=config["api_key"], base_url=config["base_url"], timeout=settings.ai_timeout_seconds)
        return provider, config

    async def chat(self, role: str, messages, *, json_mode=False, temperature=None):
        provider, config = self.provider_for(role)
        if not config["api_key"]:
            raise ProviderError(f"{role.title()} AI is not configured. Add {role.upper()}_AI_API_KEY to backend/.env.")
        models = [config["model"], *config.get("fallback_models", [])]
        last_error = None
        for model in dict.fromkeys(m for m in models if m):
            for attempt in range(settings.ai_retry_count + 1):
                try:
                    return await provider.chat(messages, model=model, temperature=config["temperature"] if temperature is None else temperature, response_format="json" if json_mode else None)
                except ProviderError as exc:
                    last_error = exc
                    if not exc.retryable or attempt >= settings.ai_retry_count: break
                    await asyncio.sleep(settings.ai_retry_delay_seconds * (2 ** attempt))
        raise ProviderError(f"{role.title()} AI failed. Last error: {last_error}", retryable=getattr(last_error, "retryable", False))

    async def stream(self, role: str, messages, *, temperature=None):
        provider, config = self.provider_for(role)
        if not config["api_key"]:
            raise ProviderError(f"{role.title()} AI is not configured. Add {role.upper()}_AI_API_KEY to backend/.env.")
        models = list(dict.fromkeys(m for m in [config["model"], *config.get("fallback_models", [])] if m))
        last_error = None
        for model in models:
            try:
                async for chunk in provider.stream_chat(messages, model=model, temperature=config["temperature"] if temperature is None else temperature):
                    yield chunk
                return
            except ProviderError as exc:
                last_error = exc
                if not exc.retryable: raise
        raise ProviderError(f"{role.title()} AI failed during streaming. Last error: {last_error}", retryable=getattr(last_error, "retryable", False))

ai_manager = AIManager()
