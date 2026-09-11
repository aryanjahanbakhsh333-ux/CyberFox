from flask import Blueprint, jsonify

from production_readiness import (
    check_production_environment
)

from monitoring_service import (
    build_monitoring_status
)


production_api = Blueprint(
    "production_api",
    __name__,
    url_prefix="/api/system"
)


@production_api.get("/readiness")
def readiness():
    result = check_production_environment()

    return jsonify({
        "success": True,
        **result
    })


@production_api.get("/monitoring")
def monitoring():
    return jsonify({
        "success": True,
        **build_monitoring_status()
    })
