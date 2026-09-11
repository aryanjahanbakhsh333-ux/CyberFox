import os


class PayoutConfig:

    PAYOUT_PROVIDER = os.getenv(
        "PAYOUT_PROVIDER",
        "stripe"
    )

    PAYOUT_ACCOUNT_ID = os.getenv(
        "PAYOUT_ACCOUNT_ID",
        ""
    )

    PAYOUT_CURRENCY = os.getenv(
        "PAYOUT_CURRENCY",
        "usd"
    )

    PAYOUT_COUNTRY = os.getenv(
        "PAYOUT_COUNTRY",
        ""
    )

    PAYOUTS_ENABLED = (
        os.getenv(
            "PAYOUTS_ENABLED",
            "false"
        ).lower()
        == "true"
    )
