from flask import Blueprint, jsonify

from production_runtime_guard import (
    ProductionRuntimeGuard
)


production_runtime_api = Blueprint(
    "production_runtime_api",
    __name__,
    url_prefix="/api/system"
)


@production_runtime_api.get("/runtime")
def runtime():
    result = ProductionRuntimeGuard().check()

    status_code = (
        200
        if result["ready"]
        else 503
    )

    return jsonify({
        "success": result["ready"],
        **result
    }), status_code
