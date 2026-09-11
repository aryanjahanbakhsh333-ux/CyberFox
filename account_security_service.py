from database import db
from account_security_model import (
    AccountSecurity
)


def get_security_record(user_id):

    record = AccountSecurity.query.filter_by(
        user_id=user_id
    ).first()

    if record:
        return record

    record = AccountSecurity(
        user_id=user_id,
        email_verified=False,
        two_factor_enabled=False
    )

    db.session.add(record)
    db.session.commit()

    return record


def verify_email(user_id):

    record = get_security_record(
        user_id
    )

    record.email_verified = True

    db.session.commit()

    return record


def enable_2fa(user_id):

    record = get_security_record(
        user_id
    )

    record.two_factor_enabled = True

    db.session.commit()

    return record


def disable_2fa(user_id):

    record = get_security_record(
        user_id
    )

    record.two_factor_enabled = False

    db.session.commit()

    return record
