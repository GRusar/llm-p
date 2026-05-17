from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url.rstrip("/")

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }
        payload: dict[str, Any] = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            async with httpx.AsyncClient(base_url=f"{self._base_url}/", timeout=60.0) as client:
                response = await client.post("chat/completions", json=payload, headers=headers)
        except httpx.HTTPError as exc:
            raise ExternalServiceError("OpenRouter request failed") from exc

        if response.status_code >= 400:
            raise ExternalServiceError(
                f"OpenRouter returned status {response.status_code}"
            )

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ExternalServiceError("OpenRouter response has unexpected format") from exc

        if not isinstance(content, str):
            raise ExternalServiceError("OpenRouter response content is invalid")

        return content
