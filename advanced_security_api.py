from flask import Blueprint, jsonify, request

from models import User
from session_service import get_session

from security_center_v2 import (
    advanced_security_center
)

from device_security import device_security
from server_security import server_security
from defense_engine import defense_engine


advanced_security_api = Blueprint(
    "advanced_security_api",
    __name__,
    url_prefix="/api/advanced-security"
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

    session = get_session(
        token
    )

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@advanced_security_api.post("/analyze")
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

    result = advanced_security_center.analyze(
        data
    )

    return jsonify(result)


@advanced_security_api.post("/device")
def device():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    result = device_security.inspect(
        data
    )

    return jsonify(result)


@advanced_security_api.post("/server")
def server():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    result = server_security.inspect_authorized_server(
        user,
        data
    )

    return jsonify(result)


@advanced_security_api.post("/defense/recommend")
def defense_recommend():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if user.plan != "pro":
        return jsonify({
            "success": False,
            "error": "Pro plan required."
        }), 403

    data = request.get_json(
        silent=True
    ) or {}

    findings = data.get(
        "findings",
        []
    )

    result = defense_engine.recommend_actions(
        findings
    )

    return jsonify(result)
