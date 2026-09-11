from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_usage_guard import (
    AIUsageGuard
)


ai_usage_api = Blueprint(
    "ai_usage_api",
    __name__,
    url_prefix="/api/ai"
)

usage_guard = AIUsageGuard()


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


@ai_usage_api.get("/usage")
def usage():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error":
                "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "plan": user.plan,
        **usage_guard.status(
            user.id,
            user.plan
        )
    })
