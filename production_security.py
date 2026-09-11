import os


def validate_production_environment():
    problems = []

    environment = os.getenv(
        "APP_ENV",
        "development"
    )

    secret_key = os.getenv(
        "SECRET_KEY",
        ""
    )

    if environment == "production":

        if not secret_key:
            problems.append(
                "SECRET_KEY is missing."
            )

        if secret_key in {
            "change-this-secret-key",
            "replace-with-a-long-random-secret"
        }:
            problems.append(
                "SECRET_KEY must be changed."
            )

    return {
        "secure": len(problems) == 0,
        "environment": environment,
        "problems": problems
    }
