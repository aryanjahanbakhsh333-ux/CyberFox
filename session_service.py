import secrets
from datetime import datetime, timedelta


SESSIONS = {}


SESSION_DURATION_HOURS = 24


def create_session(user_id):
    token = secrets.token_urlsafe(32)

    expires_at = (
        datetime.utcnow()
        + timedelta(hours=SESSION_DURATION_HOURS)
    )

    SESSIONS[token] = {
        "user_id": user_id,
        "expires_at": expires_at
    }

    return token


def get_session(token):
    if not token:
        return None

    session = SESSIONS.get(token)

    if not session:
        return None

    if datetime.utcnow() >= session["expires_at"]:
        SESSIONS.pop(token, None)
        return None

    return session


def delete_session(token):
    if token:
        SESSIONS.pop(token, None)
