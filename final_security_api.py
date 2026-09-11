from flask import Blueprint, jsonify, request

from ai_engine import AISecurityEngine
from phishing_detector import detect_phishing
from scam_hunter import scan_scam_text
from threat_prediction_service import predict_threat

final_security_api = Blueprint(
    "final_security_api",
    __name__,
    url_prefix="/api/final-security"
)


def _auth_user():
    from models import User
    from session_service import get_session

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


@final_security_api.post("/scan")
def scan():
    user = _auth_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    text = str(
        data.get("text", "")
    ).strip()

    if not text:
        return jsonify({
            "success": False,
            "error": "Text is required."
        }), 400

    phishing = detect_phishing(text)
    scam = scan_scam_text(text)

    findings = []

    if phishing.get("is_phishing"):
        findings.append({
            "type": "phishing",
            "severity": "high"
        })

    if scam.get("suspicious"):
        findings.append({
            "type": "scam",
            "severity": "high"
        })

    prediction = predict_threat(
        findings
    )

    return jsonify({
        "success": True,
        "phishing": phishing,
        "scam": scam,
        "prediction": prediction
    })


@final_security_api.post("/ai")
def ai_analysis():
    user = _auth_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    findings = data.get(
        "findings",
        []
    )

    if not isinstance(findings, list):
        return jsonify({
            "success": False,
            "error": "findings must be a list."
        }), 400

    engine = AISecurityEngine()

    result = engine.analyze(
        data
    )

    prediction = predict_threat(
        findings
    )

    return jsonify({
        "success": True,
        "analysis": result,
        "prediction": prediction
    })
