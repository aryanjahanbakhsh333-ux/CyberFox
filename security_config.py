import os


class SecurityConfig:

    SESSION_COOKIE_NAME = os.getenv(
        "SESSION_COOKIE_NAME",
        "security_session"
    )

    SESSION_COOKIE_SECURE = (
        os.getenv(
            "SESSION_COOKIE_SECURE",
            "true"
        ).lower() == "true"
    )

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = os.getenv(
        "SESSION_COOKIE_SAMESITE",
        "Lax"
    )

    MAX_LOGIN_ATTEMPTS = int(
        os.getenv(
            "MAX_LOGIN_ATTEMPTS",
            "5"
        )
    )

    LOGIN_LOCKOUT_MINUTES = int(
        os.getenv(
            "LOGIN_LOCKOUT_MINUTES",
            "15"
        )
    )

    PASSWORD_MIN_LENGTH = int(
        os.getenv(
            "PASSWORD_MIN_LENGTH",
            "8"
        )
    )
