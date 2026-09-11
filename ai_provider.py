import os

from urllib import request
from urllib import error

import json


class AIProviderError(Exception):
    pass


class AIProvider:

    def __init__(self):
        self.api_key = os.getenv(
            "AI_API_KEY",
            ""
        )

        self.base_url = os.getenv(
            "AI_API_URL",
            ""
        )

        self.model = os.getenv(
            "AI_MODEL",
            ""
        )

    def is_configured(self):
        return bool(
            self.api_key
            and self.base_url
            and self.model
        )

    def analyze(self, system_prompt, user_prompt):
        if not self.is_configured():
            raise AIProviderError(
                "AI provider is not configured."
            )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }

        data = json.dumps(
            payload
        ).encode("utf-8")

        request_object = request.Request(
            self.base_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {self.api_key}"
                )
            },
            method="POST"
        )

        try:
            with request.urlopen(
                request_object,
                timeout=30
            ) as response:

                response_data = json.loads(
                    response.read().decode("utf-8")
                )

                return response_data

        except error.HTTPError as exc:
            raise AIProviderError(
                "AI provider returned an HTTP error."
            ) from exc

        except error.URLError as exc:
            raise AIProviderError(
                "Unable to connect to AI provider."
            ) from exc

        except Exception as exc:
            raise AIProviderError(
                "AI provider request failed."
            ) from exc
