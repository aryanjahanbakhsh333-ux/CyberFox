import os


class ProductionRuntimeGuard:
    REQUIRED = (
        "SECRET_KEY",
        "DATABASE_URL",
    )

    def check(self):
        environment = os.getenv(
            "APP_ENV",
            "development"
        ).lower()

        missing = []

        for variable in self.REQUIRED:
            value = os.getenv(variable, "").strip()

            if not value:
                missing.append(variable)

        if environment == "production":
            secret = os.getenv(
                "SECRET_KEY",
                ""
            )

            if len(secret) < 32:
                return {
                    "ready": False,
                    "environment": environment,
                    "missing": missing,
                    "error":
                        "Production SECRET_KEY must be at least 32 characters."
                }

        return {
            "ready": len(missing) == 0,
            "environment": environment,
            "missing": missing
        }
