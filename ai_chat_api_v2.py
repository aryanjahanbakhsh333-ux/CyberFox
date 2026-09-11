from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_chat_service import (
    SecurityChatService
)


ai_chat_api_v2 = Blueprint(
    "ai_chat_api_v2",
    __name__,
    url_prefix="/api/ai-chat"
)


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


@ai_chat_api_v2.post("/")
def chat():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    message = data.get(
        "message",
        ""
    )

    conversation = data.get(
        "conversation",
        []
    )

    if not isinstance(
        conversation,
        list
    ):
        conversation = []

    service = SecurityChatService()

    result = service.answer(
        message=message,
        conversation=conversation
    )

    return jsonify(result)
