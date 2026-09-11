from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User
from session_service import get_session
from plan_service import get_plan_features


billing_api = Blueprint(
    "billing_api",
    __name__,
    url_prefix="/api/billing"
)


def get_current_user():
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


@billing_api.get("/status")
def billing_status():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "plan": user.plan,
        "features": get_plan_features(
            user.plan
        )
    })
