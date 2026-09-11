from flask import (
    Blueprint,
    jsonify,
    request
)

from scanner_service import (
    scan_url,
    scan_message
)


scanner_api = Blueprint(
    "scanner_api",
    __name__,
    url_prefix="/api/scanner"
)


@scanner_api.post("/url")
def scan_url_endpoint():

    data = request.get_json(
        silent=True
    ) or {}

    url = data.get(
        "url",
        ""
    )

    if not url:
        return jsonify({
            "success": False,
            "error": "URL is required."
        }), 400

    return jsonify(
        scan_url(url)
    )


@scanner_api.post("/message")
def scan_message_endpoint():

    data = request.get_json(
        silent=True
    ) or {}

    text = data.get(
        "text",
        ""
    )

    if not text:
        return jsonify({
            "success": False,
            "error": "Message is required."
        }), 400

    return jsonify(
        scan_message(text)
    )
