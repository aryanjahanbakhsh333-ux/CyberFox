from functools import wraps

from flask import jsonify, request

from models import User
from session_service import get_session


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


def pro_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if not user:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        if user.plan != "pro":
            return jsonify({
                "success": False,
                "error": "Pro subscription required."
            }), 403

        return function(
            user,
            *args,
            **kwargs
        )

    return wrapper
