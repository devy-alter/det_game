from abc import ABC, abstractmethod
from typing import AsyncIterator

class ProviderError(RuntimeError):
    def __init__(self, message: str, *, retryable: bool = False):
        super().__init__(message)
        self.retryable = retryable

class LLMProvider(ABC):
    def __init__(self, *, api_key: str, base_url: str, timeout: float = 60.0):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]], *, model: str, temperature: float = .7, response_format: str | None = None) -> str:
        raise NotImplementedError

    async def stream_chat(self, messages: list[dict[str, str]], *, model: str, temperature: float = .7):
        yield await self.chat(messages, model=model, temperature=temperature)
