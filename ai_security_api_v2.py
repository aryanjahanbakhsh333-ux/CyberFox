from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_security_orchestrator import (
    AISecurityOrchestrator
)

from ai_security_report import (
    build_ai_report
)


ai_security_api_v2 = Blueprint(
    "ai_security_api_v2",
    __name__,
    url_prefix="/api/ai-security"
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


@ai_security_api_v2.post("/analyze")
def analyze():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    target = data.get(
        "target",
        "unknown"
    )

    findings = data.get(
        "findings",
        []
    )

    if not isinstance(findings, list):
        return jsonify({
            "success": False,
            "error":
                "findings must be a list."
        }), 400

    orchestrator = (
        AISecurityOrchestrator()
    )

    ai_result = orchestrator.analyze(
        target=target,
        findings=findings,
        context=data.get(
            "context",
            {}
        )
    )

    report = build_ai_report(
        target=target,
        findings=findings,
        ai_analysis=ai_result
    )

    return jsonify({
        "success": True,
        "report": report
    })
