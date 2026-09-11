from flask import Blueprint, jsonify, request

from models import User
from plan_service import get_plan_features
from session_service import get_session


plan_api = Blueprint(
    "plan_api",
    __name__,
    url_prefix="/api/plans"
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


@plan_api.get("/current")
def current_plan():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "plan": user.plan,
        "features": get_plan_features(user.plan)
    })
