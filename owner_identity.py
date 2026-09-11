import os


def get_configured_owner_email():
    return os.getenv(
        "OWNER_EMAIL",
        ""
    ).strip().lower()


def is_configured_owner_email(email):
    if not email:
        return False

    owner_email = get_configured_owner_email()

    if not owner_email:
        return False

    return email.strip().lower() == owner_email


def get_owner_welcome():
    return {
        "title": "WELCOME",
        "message": "Welcome, Owner.",
        "system": "Cybersecurity AI Platform"
    }
