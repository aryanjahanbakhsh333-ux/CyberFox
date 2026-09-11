from flask import Blueprint, jsonify, request

from models import User
from security_service import analyze_target
from session_service import get_session


security_api = Blueprint(
    "security_api",
    __name__,
    url_prefix="/api/security"
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

    return User.query.get(session["user_id"])


@security_api.post("/analyze")
def analyze():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    target_type = data.get(
        "type",
        ""
    )

    result = analyze_target(
        user,
        target_type
    )

    return jsonify(result)
