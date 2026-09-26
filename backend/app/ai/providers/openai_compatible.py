import json
import asyncio

import httpx

from app.ai.providers.base import LLMProvider, ProviderError


TRANSIENT_HTTP_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}


class OpenAICompatibleProvider(LLMProvider):
    async def chat(self, messages, *, model, temperature=0.7, response_format=None):
        if not self.api_key:
            raise ProviderError("API key is not configured for this AI role")

        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if "openrouter.ai" in self.base_url.lower():
            headers["HTTP-Referer"] = "http://localhost:5173"
            headers["X-Title"] = "Detective Game"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise ProviderError(
                f"AI provider timed out while calling model '{model}'", retryable=True
            ) from exc
        except httpx.HTTPError as exc:
            raise ProviderError(
                f"AI provider connection failed for model '{model}': {exc}",
                retryable=True,
            ) from exc

        if response.status_code >= 400:
            retryable = response.status_code in TRANSIENT_HTTP_STATUS
            detail = response.text[:700]
            raise ProviderError(
                f"AI provider returned HTTP {response.status_code} for model '{model}': {detail}",
                retryable=retryable,
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise ProviderError(
                f"AI provider returned invalid JSON for model '{model}'", retryable=True
            ) from exc

        if isinstance(data, dict) and data.get("error"):
            error = data.get("error") or {}
            message = error.get("message") or "Unknown upstream provider error"
            code = error.get("code")
            retryable = str(code) in {"408", "409", "425", "429", "500", "502", "503", "504"} or "overload" in message.lower() or "temporarily" in message.lower()
            suffix = f" (code {code})" if code is not None else ""
            raise ProviderError(
                f"Upstream error from provider for model '{model}': {message}{suffix}",
                retryable=retryable,
            )

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"Unexpected provider response for model '{model}': {data}") from exc

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    text_parts.append(item["text"])
            content = "".join(text_parts)

        if not isinstance(content, str) or not content.strip():
            raise ProviderError(f"AI provider returned an empty response for model '{model}'")
        return content.strip()

    async def stream_chat(self, messages, *, model, temperature=0.7):
        if not self.api_key:
            raise ProviderError("API key is not configured for this AI role")
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {"model": model, "messages": messages, "temperature": temperature, "stream": True}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        if "openrouter.ai" in self.base_url.lower():
            headers["HTTP-Referer"] = "http://localhost:5173"
            headers["X-Title"] = "Detective Game"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code >= 400:
                        body = (await response.aread()).decode("utf-8", errors="replace")[:700]
                        retryable = response.status_code in TRANSIENT_HTTP_STATUS
                        raise ProviderError(f"AI provider returned HTTP {response.status_code} for model '{model}': {body}", retryable=retryable)
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        raw = line[5:].strip()
                        if raw == "[DONE]":
                            break
                        try:
                            data = json.loads(raw)
                        except ValueError:
                            continue
                        if isinstance(data, dict) and data.get("error"):
                            error = data.get("error") or {}
                            message = error.get("message") or "Unknown upstream provider error"
                            code = error.get("code")
                            retryable = str(code) in {"408","409","425","429","500","502","503","504"} or "overload" in message.lower() or "temporarily" in message.lower()
                            raise ProviderError(f"Upstream error from provider for model '{model}': {message}", retryable=retryable)
                        choice = (data.get("choices") or [{}])[0]
                        delta = choice.get("delta") or {}
                        text = delta.get("content")
                        if isinstance(text, str) and text:
                            yield text
        except ProviderError:
            raise
        except httpx.TimeoutException as exc:
            raise ProviderError(f"AI provider timed out while streaming model '{model}'", retryable=True) from exc
        except httpx.HTTPError as exc:
            raise ProviderError(f"AI provider connection failed while streaming model '{model}': {exc}", retryable=True) from exc
