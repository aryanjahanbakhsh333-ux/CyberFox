import os

from models import User


def get_owner_email():
    return os.getenv("OWNER_EMAIL", "").strip().lower()


def is_owner(user):
    if not user:
        return False

    owner_email = get_owner_email()

    if not owner_email:
        return False

    return (
        user.email.lower() == owner_email
        and user.role == "owner"
    )


def get_owner_status(user):
    return {
        "is_owner": is_owner(user),
        "role": user.role if user else None
    }
