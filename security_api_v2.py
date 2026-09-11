from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_security_service import (
    analyze_security_context
)


security_api_v2 = Blueprint(
    "security_api_v2",
    __name__,
    url_prefix="/api/security-v2"
)


@security_api_v2.post("/ai-analyze")
def ai_analyze():

    data = request.get_json(
        silent=True
    ) or {}

    if not isinstance(
        data,
        dict
    ):
        return jsonify({
            "success": False,
            "error": "Invalid security context."
        }), 400

    result = analyze_security_context(
        data
    )

    status_code = 200

    if not result.get(
        "success",
        False
    ):
        status_code = 503

    return jsonify(
        result
    ), status_code
