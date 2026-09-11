from flask import Blueprint, jsonify, request

from models import User
from password_service import change_password
from session_service import get_session


password_api = Blueprint(
    "password_api",
    __name__,
    url_prefix="/api/user/password"
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


@password_api.post("/change")
def change():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    current_password = data.get(
        "current_password",
        ""
    )

    new_password = data.get(
        "new_password",
        ""
    )

    success, error = change_password(
        user,
        current_password,
        new_password
    )

    if not success:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Password changed successfully."
    })
