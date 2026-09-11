from recovery_ai_service import (
    RecoveryAIService
)


class PasswordRecovery:

    def __init__(self):
        self.ai = RecoveryAIService()

    def start(
        self,
        provider,
        authorized=False
    ):
        if not authorized:
            return {
                "success": False,
                "error":
                    "Authorization is required."
            }

        return self.ai.analyze(
            recovery_type="password",
            provider=provider
        )
