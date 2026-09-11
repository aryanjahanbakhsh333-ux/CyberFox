from flask import Blueprint, jsonify

from ai_health_service import (
    get_ai_health
)


ai_health_api = Blueprint(
    "ai_health_api",
    __name__,
    url_prefix="/api/ai"
)


@ai_health_api.get("/health")
def health():
    return jsonify({
        "success": True,
        **get_ai_health()
    })
