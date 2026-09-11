import secrets
from datetime import datetime, timedelta


TWO_FACTOR_CODES = {}


def create_2fa_code(
    user_id,
    expires_minutes=5
):
    code = str(
        secrets.randbelow(1000000)
    ).zfill(6)

    TWO_FACTOR_CODES[user_id] = {
        "code": code,
        "expires_at": (
            datetime.utcnow()
            + timedelta(
                minutes=expires_minutes
            )
        )
    }

    return code


def verify_2fa_code(
    user_id,
    code
):
    record = TWO_FACTOR_CODES.get(
        user_id
    )

    if not record:
        return False

    if datetime.utcnow() >= record[
        "expires_at"
    ]:
        TWO_FACTOR_CODES.pop(
            user_id,
            None
        )

        return False

    if str(code) != record["code"]:
        return False

    TWO_FACTOR_CODES.pop(
        user_id,
        None
    )

    return True
