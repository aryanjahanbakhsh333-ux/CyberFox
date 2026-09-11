import json
from datetime import datetime

from database import db
from auth_security_model import AuthSecurity

from recovery_code_service import (
    generate_recovery_codes,
    hash_recovery_codes,
    consume_recovery_code
)

from totp_service import (
    generate_totp_secret,
    verify_totp
)


def get_auth_security(user_id):
    record = AuthSecurity.query.filter_by(
        user_id=user_id
    ).first()

    if record:
        return record

    record = AuthSecurity(
        user_id=user_id,
        totp_enabled=False
    )

    db.session.add(record)
    db.session.commit()

    return record


def start_totp_setup(user_id):
    record = get_auth_security(user_id)

    if record.totp_enabled:
        return {
            "success": False,
            "error": "TOTP is already enabled."
        }

    secret = generate_totp_secret()

    record.totp_secret = secret

    db.session.commit()

    return {
        "success": True,
        "secret": secret
    }


def enable_totp(
    user_id,
    code
):
    record = get_auth_security(user_id)

    if not record.totp_secret:
        return {
            "success": False,
            "error": "TOTP setup has not been started."
        }

    if not verify_totp(
        record.totp_secret,
        code
    ):
        return {
            "success": False,
            "error": "Invalid authentication code."
        }

    recovery_codes = generate_recovery_codes()

    record.totp_enabled = True

    record.recovery_codes = json.dumps(
        hash_recovery_codes(
            recovery_codes
        )
    )

    record.last_2fa_at = datetime.utcnow()

    db.session.commit()

    return {
        "success": True,
        "recovery_codes": recovery_codes
    }


def verify_two_factor(
    user_id,
    code
):
    record = get_auth_security(user_id)

    if not record.totp_enabled:
        return False

    if verify_totp(
        record.totp_secret,
        code
    ):
        record.last_2fa_at = datetime.utcnow()
        db.session.commit()

        return True

    return False


def verify_recovery_code(
    user_id,
    code
):
    record = get_auth_security(user_id)

    if not record.recovery_codes:
        return False

    try:
        hashed_codes = json.loads(
            record.recovery_codes
        )
    except (TypeError, ValueError):
        return False

    valid, remaining = consume_recovery_code(
        code,
        hashed_codes
    )

    if not valid:
        return False

    record.recovery_codes = json.dumps(
        remaining
    )

    record.last_2fa_at = datetime.utcnow()

    db.session.commit()

    return True


def disable_totp(user_id):
    record = get_auth_security(user_id)

    record.totp_enabled = False
    record.totp_secret = None
    record.recovery_codes = None

    db.session.commit()

    return True
