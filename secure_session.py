import secrets
from datetime import datetime, timedelta


class SecureSessionStore:

    def __init__(self):
        self.sessions = {}

    def create(
        self,
        user_id,
        duration_hours=24
    ):
        token = secrets.token_urlsafe(48)

        expires_at = (
            datetime.utcnow()
            + timedelta(
                hours=duration_hours
            )
        )

        self.sessions[token] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at
        }

        return token

    def get(self, token):
        if not token:
            return None

        session = self.sessions.get(
            token
        )

        if not session:
            return None

        if datetime.utcnow() >= session[
            "expires_at"
        ]:
            self.sessions.pop(
                token,
                None
            )

            return None

        return session

    def delete(self, token):
        if token:
            self.sessions.pop(
                token,
                None
            )

    def delete_user_sessions(
        self,
        user_id
    ):
        tokens = []

        for token, session in (
            self.sessions.items()
        ):
            if session["user_id"] == user_id:
                tokens.append(token)

        for token in tokens:
            self.sessions.pop(
                token,
                None
            )


secure_sessions = SecureSessionStore()
