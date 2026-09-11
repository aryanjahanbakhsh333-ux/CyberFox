from flask import (
    Blueprint,
    jsonify,
    request
)

from lock_recovery import (
    LockRecovery
)

from password_recovery import (
    PasswordRecovery
)


recovery_api = Blueprint(
    "recovery_api",
    __name__,
    url_prefix="/api/recovery"
)


def get_current_user():
    from models import User
    from session_service import get_session

    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith(
        "Bearer "
    ):
        return None

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@recovery_api.post("/lock")
def lock_recovery():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error":
                "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    result = LockRecovery().analyze(
        lock_type=data.get(
            "lock_type",
            ""
        ),
        provider=data.get(
            "provider",
            "unknown"
        ),
        authorized=True
    )

    return jsonify(result)


@recovery_api.post("/password")
def password_recovery():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error":
                "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    result = PasswordRecovery().start(
        provider=data.get(
            "provider",
            "unknown"
        ),
        authorized=True
    )

    return jsonify(result)
