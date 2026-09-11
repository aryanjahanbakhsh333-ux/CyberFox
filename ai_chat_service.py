from ai_provider_real import (
    HTTPAIProvider,
    AIProviderError
)


CHAT_SYSTEM_PROMPT = """
You are the security assistant of a defensive
cybersecurity platform.

Give clear, practical and safe security advice.

The user should only analyze or protect systems,
accounts, devices or servers they own or are
authorized to manage.

Never request passwords, API secrets, payment-card
numbers, recovery codes or other credentials.

Do not provide instructions for unauthorized access,
credential theft, malware, destructive attacks or
bypassing security controls.
"""


class SecurityChatService:

    def __init__(self):
        self.provider = HTTPAIProvider()

    def answer(
        self,
        message,
        conversation=None
    ):
        if not message or not message.strip():
            return {
                "success": False,
                "error": "Message cannot be empty."
            }

        messages = [
            {
                "role": "system",
                "content": CHAT_SYSTEM_PROMPT
            }
        ]

        if conversation:
            for item in conversation[-10:]:
                role = item.get("role")
                content = item.get("content")

                if role in {"user", "assistant"}:
                    messages.append({
                        "role": role,
                        "content": str(content)
                    })

        messages.append({
            "role": "user",
            "content": message.strip()
        })

        if not self.provider.available():
            return {
                "success": True,
                "provider": "local",
                "reply": self._fallback(
                    message
                )
            }

        try:
            answer = self.provider.chat(
                messages
            )

            return {
                "success": True,
                "provider": "ai",
                "reply": answer
            }

        except AIProviderError:
            return {
                "success": True,
                "provider": "local",
                "reply": self._fallback(
                    message
                )
            }

    def _fallback(self, message):
        text = message.lower()

        if "phishing" in text:
            return (
                "Do not open suspicious links. "
                "Verify the sender and domain independently "
                "before entering credentials."
            )

        if "password" in text:
            return (
                "Use a unique strong password and enable "
                "two-factor authentication."
            )

        if "2fa" in text or "two factor" in text:
            return (
                "Enable an authenticator-based second factor "
                "when available and keep recovery codes offline."
            )

        if "scam" in text:
            return (
                "Do not send money or security codes under "
                "pressure. Verify the request through an "
                "independent trusted channel."
            )

        return (
            "I can help analyze security risks, phishing, "
            "privacy, account protection and defensive "
            "security configuration."
        )
