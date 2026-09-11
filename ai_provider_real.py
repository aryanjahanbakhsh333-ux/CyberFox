import os

import requests


class AIProviderError(Exception):
    pass


class HTTPAIProvider:
    def __init__(self):
        self.api_key = os.getenv(
            "AI_API_KEY",
            ""
        )

        self.base_url = os.getenv(
            "AI_BASE_URL",
            ""
        ).rstrip("/")

        self.model = os.getenv(
            "AI_MODEL",
            ""
        )

    def available(self):
        return bool(
            self.api_key
            and self.base_url
            and self.model
        )

    def chat(
        self,
        messages,
        temperature=0.2
    ):
        if not self.available():
            raise AIProviderError(
                "AI provider is not configured."
            )

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization":
                    f"Bearer {self.api_key}",
                "Content-Type":
                    "application/json"
            },
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature
            },
            timeout=30
        )

        if response.status_code >= 400:
            raise AIProviderError(
                "AI provider request failed."
            )

        data = response.json()

        choices = data.get(
            "choices",
            []
        )

        if not choices:
            raise AIProviderError(
                "AI provider returned no response."
            )

        return (
            choices[0]
            .get("message", {})
            .get("content", "")
        )
