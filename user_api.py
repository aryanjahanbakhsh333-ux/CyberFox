from flask import Blueprint, jsonify, request

from models import User
from session_service import get_session
from user_service import get_user_profile


user_api = Blueprint(
    "user_api",
    __name__,
    url_prefix="/api/user"
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


@user_api.get("/profile")
def profile():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "user": get_user_profile(user)
    })
