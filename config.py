import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.getenv(
        "APP_NAME",
        "Cybersecurity AI Platform"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    ENVIRONMENT = os.getenv(
        "APP_ENV",
        "development"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///security_platform.db"
    )

    AI_API_KEY = os.getenv(
        "AI_API_KEY",
        ""
    )

    PAYMENT_SECRET_KEY = os.getenv(
        "PAYMENT_SECRET_KEY",
        ""
    )

    PAYMENT_WEBHOOK_SECRET = os.getenv(
        "PAYMENT_WEBHOOK_SECRET",
        ""
    )

    OWNER_EMAIL = os.getenv(
        "OWNER_EMAIL",
        ""
    )
