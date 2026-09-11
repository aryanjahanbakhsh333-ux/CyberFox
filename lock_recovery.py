from recovery_ai_service import (
    RecoveryAIService
)


class LockRecovery:

    SUPPORTED = {
        "account",
        "device",
        "application",
        "email"
    }

    def __init__(self):
        self.ai = RecoveryAIService()

    def analyze(
        self,
        lock_type,
        provider,
        authorized=False
    ):
        if lock_type not in self.SUPPORTED:
            return {
                "success": False,
                "error":
                    "Unsupported recovery type."
            }

        if not authorized:
            return {
                "success": False,
                "error":
                    "Authorization is required for recovery."
            }

        return self.ai.analyze(
            recovery_type=lock_type,
            provider=provider
        )
