from flask import Blueprint, jsonify, request

from models import User
from owner_service import is_owner
from session_service import get_session


owner_api = Blueprint(
    "owner_api",
    __name__,
    url_prefix="/api/owner"
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


@owner_api.get("/status")
def owner_status():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if not is_owner(user):
        return jsonify({
            "success": False,
            "error": "Owner access required."
        }), 403

    return jsonify({
        "success": True,
        "owner": True,
        "message": "Owner access granted."
    })
