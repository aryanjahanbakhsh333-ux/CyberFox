from flask import Blueprint, jsonify, request

from models import User
from session_service import get_session
from threat_service import get_user_threats


threat_api = Blueprint(
    "threat_api",
    __name__,
    url_prefix="/api/threats"
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


@threat_api.get("/")
def threats():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    threats = get_user_threats(
        user.id
    )

    return jsonify({
        "success": True,
        "threats": [
            {
                "id": threat.id,
                "type": threat.threat_type,
                "title": threat.title,
                "description": threat.description,
                "severity": threat.severity,
                "status": threat.status,
                "created_at": (
                    threat.created_at.isoformat()
                )
            }
            for threat in threats
        ]
    })
