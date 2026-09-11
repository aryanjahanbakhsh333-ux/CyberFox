from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_final_pipeline import (
    AIFinalPipeline
)

from ai_input_sanitizer import (
    sanitize_ai_request
)

from ai_usage_guard import (
    AIUsageGuard
)


ai_final_api = Blueprint(
    "ai_final_api",
    __name__,
    url_prefix="/api/ai-final"
)

pipeline = AIFinalPipeline()
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


@ai_final_api.post("/analyze")
def analyze():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error":
                "Authentication required."
        }), 401

    if not usage_guard.allowed(
        user.id,
        user.plan
    ):
        return jsonify({
            "success": False,
            "error":
                "AI daily usage limit reached."
        }), 429

    data = sanitize_ai_request(
        request.get_json(
            silent=True
        ) or {}
    )

    result = pipeline.analyze(
        target=data["target"],
        data=data["context"],
        message=data["message"]
    )

    usage_guard.consume(
        user.id,
        user.plan
    )

    return jsonify(result)
