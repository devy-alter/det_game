import httpx

from app.ai.providers.base import LLMProvider, ProviderError


class GeminiProvider(LLMProvider):
    def __init__(self, *, api_key: str, base_url: str = ""):
        super().__init__(api_key=api_key, base_url=base_url or "https://generativelanguage.googleapis.com")

    async def chat(self, messages, *, model, temperature=0.7, response_format=None):
        if not self.api_key:
            raise ProviderError("API key is not configured for this AI role")

        model_name = model.removeprefix("models/")
        url = f"{self.base_url.rstrip('/')}/v1beta/models/{model_name}:generateContent"

        system_parts = []
        contents = []
        for message in messages:
            role = message.get("role", "user")
            text = message.get("content", "")
            if role == "system":
                system_parts.append(text)
            else:
                contents.append({
                    "role": "model" if role == "assistant" else "user",
                    "parts": [{"text": text}],
                })

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature},
        }
        if response_format == "json":
            payload["generationConfig"]["responseMimeType"] = "application/json"
        if system_parts:
            payload["systemInstruction"] = {"parts": [{"text": "\n\n".join(system_parts)}]}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, params={"key": self.api_key}, json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Gemini connection failed: {exc}") from exc

        if response.status_code >= 400:
            raise ProviderError(
                f"Gemini returned HTTP {response.status_code}: {response.text[:500]}"
            )

        data = response.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"Unexpected Gemini response: {data}") from exc

        if not isinstance(text, str) or not text.strip():
            raise ProviderError("Gemini returned an empty response")
        return text.strip()
