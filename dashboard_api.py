from flask import Blueprint, jsonify, request

from dashboard_service import build_dashboard
from models import User
from session_service import get_session


dashboard_api = Blueprint(
    "dashboard_api",
    __name__,
    url_prefix="/api/dashboard"
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


@dashboard_api.get("/")
def dashboard():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "dashboard": build_dashboard(user)
    })
