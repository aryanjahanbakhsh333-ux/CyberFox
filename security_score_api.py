from flask import Blueprint, jsonify, request

from models import User
from session_service import get_session
from security_score import (
    calculate_security_score,
    score_level
)


score_api = Blueprint(
    "score_api",
    __name__,
    url_prefix="/api/security-score"
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


@score_api.get("/")
def score():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    security_score = calculate_security_score()

    return jsonify({
        "success": True,
        "score": security_score,
        "level": score_level(
            security_score
        )
    })
