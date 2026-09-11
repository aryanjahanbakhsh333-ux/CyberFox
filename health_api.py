from flask import Blueprint, jsonify

from health_service import get_system_health


health_api = Blueprint(
    "health_api",
    __name__,
    url_prefix="/api/system"
)


@health_api.get("/health")
def health():
    return jsonify({
        "success": True,
        **get_system_health()
    })
