import secrets
from datetime import datetime, timedelta

from database import db
from models import User
from werkzeug.security import (
    generate_password_hash
)


RESET_CODES = {}


def create_reset_code(email):

    user = User.query.filter_by(
        email=email.strip().lower()
    ).first()

    if not user:
        return None

    code = str(
        secrets.randbelow(1000000)
    ).zfill(6)

    RESET_CODES[user.id] = {
        "code": code,
        "expires_at": (
            datetime.utcnow()
            + timedelta(
                minutes=15
            )
        )
    }

    return code


def reset_password(
    user_id,
    code,
    new_password
):

    record = RESET_CODES.get(
        user_id
    )

    if not record:
        return False

    if datetime.utcnow() >= record[
        "expires_at"
    ]:
        RESET_CODES.pop(
            user_id,
            None
        )

        return False

    if str(code) != record["code"]:
        return False

    if len(new_password) < 8:
        return False

    user = User.query.get(
        user_id
    )

    if not user:
        return False

    user.password_hash = (
        generate_password_hash(
            new_password
        )
    )

    db.session.commit()

    RESET_CODES.pop(
        user_id,
        None
    )

    return True
