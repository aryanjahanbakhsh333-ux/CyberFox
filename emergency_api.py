from flask import Blueprint, jsonify, request

from emergency_service import emergency_security
from models import User
from session_service import get_session


emergency_api = Blueprint(
    "emergency_api",
    __name__,
    url_prefix="/api/emergency"
)


def get_current_user():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@emergency_api.post("/activate")
def activate():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    result = emergency_security.activate(
        user.id
    )

    return jsonify(result)
