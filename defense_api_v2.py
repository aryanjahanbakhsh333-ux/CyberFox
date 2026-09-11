from flask import (
    Blueprint,
    jsonify,
    request
)

from defense_execution_service import (
    execute_defensive_action,
    DefenseExecutionError
)

from plan_service import is_pro_user

defense_api_v2 = Blueprint(
    "defense_api_v2",
    __name__,
    url_prefix="/api/defense-v2"
)


@defense_api_v2.post("/execute")
def execute():
    from models import User
    from session_service import get_session

    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return jsonify({
            "success": False,
            "error": "Invalid session."
        }), 401

    user = User.query.get(
        session["user_id"]
    )

    if not user or not is_pro_user(user):
        return jsonify({
            "success": False,
            "error": "Pro plan required."
        }), 403

    data = request.get_json(
        silent=True
    ) or {}

    action = str(
        data.get("action", "")
    ).strip()

    authorized = bool(
        data.get("authorized", False)
    )

    confirmed = bool(
        data.get("confirmed", False)
    )

    try:
        result = execute_defensive_action(
            action=action,
            authorized=authorized,
            confirmed=confirmed
        )

    except DefenseExecutionError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 403

    return jsonify({
        "success": True,
        **result
    })
