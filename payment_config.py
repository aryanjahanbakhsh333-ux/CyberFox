import os


class PaymentConfig:
    PROVIDER = os.getenv(
        "PAYMENT_PROVIDER",
        "stripe"
    )

    CURRENCY = os.getenv(
        "PAYMENT_CURRENCY",
        "usd"
    )

    PRO_PRICE_ID = os.getenv(
        "PRO_PRICE_ID",
        ""
    )

    PAYMENT_SECRET_KEY = os.getenv(
        "PAYMENT_SECRET_KEY",
        ""
    )

    PAYMENT_WEBHOOK_SECRET = os.getenv(
        "PAYMENT_WEBHOOK_SECRET",
        ""

    SUCCESS_URL = os.getenv(
        "PAYMENT_SUCCESS_URL",
        "/dashboard?payment=success"
    )

    CANCEL_URL = os.getenv(
        "PAYMENT_CANCEL_URL",
        "/dashboard?payment=cancelled"
    )
