import os


REQUIRED_PRODUCTION_VARS = [
    "SECRET_KEY",
    "DATABASE_URL",
]


def check_production_environment():
    environment = os.getenv(
        "APP_ENV",
        "development"
    )

    missing = []

    for variable in REQUIRED_PRODUCTION_VARS:
        value = os.getenv(variable)

        if not value:
            missing.append(variable)

    secret = os.getenv(
        "SECRET_KEY",
        ""
    )

    warnings = []

    if secret in {
        "",
        "change-this-secret-key",
        "replace-with-a-long-random-secret"
    }:
        warnings.append(
            "A production-grade SECRET_KEY is required."
        )

    if environment == "production":
        ready = (
            len(missing) == 0
            and len(warnings) == 0
        )
    else:
        ready = True

    return {
        "environment": environment,
        "ready": ready,
        "missing_variables": missing,
        "warnings": warnings
    }
