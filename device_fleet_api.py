from flask import (
    Blueprint,
    jsonify,
    request
)

from device_fleet_service import (
    register_device,
    get_user_devices,
    serialize_device
)

from session_service import get_session
from models import User


device_fleet_api = Blueprint(
    "device_fleet_api",
    __name__,
    url_prefix="/api/devices"
)


def current_user():
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


@device_fleet_api.get("/")
def devices():
    user = current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    items = get_user_devices(
        user.id
    )

    return jsonify({
        "success": True,
        "devices": [
            serialize_device(item)
            for item in items
        ]
    })


@device_fleet_api.post("/")
def add_device():
    user = current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    device_id = str(
        data.get("device_id", "")
    ).strip()

    name = str(
        data.get("name", "")
    ).strip()

    platform = str(
        data.get("platform", "")
    ).strip()

    if not device_id or not name:
        return jsonify({
            "success": False,
            "error":
                "device_id and name are required."
        }), 400

    device = register_device(
        user.id,
        device_id,
        name,
        platform
    )

    return jsonify({
        "success": True,
        "device":
            serialize_device(device)
    }), 201
