from flask import (
    Blueprint,
    jsonify,
    request
)

from security_report_service import (
    build_security_report
)

security_report_api = Blueprint(
    "security_report_api",
    __name__,
    url_prefix="/api/security-report"
)


@security_report_api.get("/")
def report():
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

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "report": build_security_report(
            user=user,
            score=20,
            threats=[],
            prediction={
                "score": 0,
                "level": "low"
            },
            recommendations=[
                "Enable two-factor authentication.",
                "Review recent account activity.",
                "Keep devices and applications updated."
            ]
        )
    })
