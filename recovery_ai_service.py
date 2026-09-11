from ai_provider_real import (
    HTTPAIProvider,
    AIProviderError
)


RECOVERY_PROMPT = """
You are a defensive account and device recovery assistant.

Help a user recover access only through legitimate
recovery procedures.

You may:
- identify the likely type of lock
- explain official recovery options
- organize recovery steps
- recommend contacting the official provider
- help create a new strong password after recovery

Never:
- guess or crack passwords
- brute-force PINs
- bypass authentication
- extract saved credentials
- defeat device security
- access an account without authorization

Never ask the user to provide a password,
PIN, recovery code, API key or payment secret.
"""


class RecoveryAIService:

    def __init__(self):
        self.provider = HTTPAIProvider()

    def analyze(self, recovery_type, provider):
        prompt = {
            "recovery_type": recovery_type,
            "provider": provider
        }

        if not self.provider.available():
            return self._fallback(
                recovery_type,
                provider
            )

        try:
            answer = self.provider.chat([
                {
                    "role": "system",
                    "content": RECOVERY_PROMPT
                },
                {
                    "role": "user",
                    "content": str(prompt)
                }
            ])

            return {
                "success": True,
                "provider": "ai",
                "answer": answer
            }

        except AIProviderError:
            return self._fallback(
                recovery_type,
                provider
            )

    def _fallback(
        self,
        recovery_type,
        provider
    ):
        return {
            "success": True,
            "provider": "local",
            "recovery_type": recovery_type,
            "provider_name": provider,
            "steps": [
                "Confirm that you own or are authorized to recover the account or device.",
                "Use the official recovery page or recovery mechanism.",
                "Complete the provider's identity verification.",
                "Create a new unique password after successful recovery.",
                "Enable two-factor authentication."
            ]
        }
