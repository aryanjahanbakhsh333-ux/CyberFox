import secrets
from datetime import datetime, timedelta


VERIFICATION_CODES = {}


def create_verification_code(
    user_id,
    expires_minutes=15
):
    code = str(
        secrets.randbelow(1000000)
    ).zfill(6)

    VERIFICATION_CODES[user_id] = {
        "code": code,
        "expires_at": (
            datetime.utcnow()
            + timedelta(
                minutes=expires_minutes
            )
        )
    }

    return code


def verify_code(
    user_id,
    code
):
    record = VERIFICATION_CODES.get(
        user_id
    )

    if not record:
        return False

    if datetime.utcnow() >= record[
        "expires_at"
    ]:
        VERIFICATION_CODES.pop(
            user_id,
            None
        )

        return False

    if str(code) != record["code"]:
        return False

    VERIFICATION_CODES.pop(
        user_id,
        None
    )

    return True


def delete_verification_code(user_id):
    VERIFICATION_CODES.pop(
        user_id,
        None
    )
