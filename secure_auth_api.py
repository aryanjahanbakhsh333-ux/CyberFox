from flask import (
    Blueprint,
    jsonify,
    request
)

from secure_auth_service import secure_login
from secure_session import secure_sessions


secure_auth_api = Blueprint(
    "secure_auth_api",
    __name__,
    url_prefix="/api/secure-auth"
)


@secure_auth_api.post("/login")
def login():

    data = request.get_json(
        silent=True
    ) or {}

    email = data.get(
        "email",
        ""
    )

    password = data.get(
        "password",
        ""
    )

    if not email or not password:
        return jsonify({
            "success": False,
            "error": (
                "Email and password are required."
            )
        }), 400

    result = secure_login(
        email,
        password
    )

    if not result["success"]:
        return jsonify(
            result
        ), 401

    return jsonify(
        result
    )


@secure_auth_api.post("/logout")
def logout():

    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if authorization.startswith(
        "Bearer "
    ):
        token = authorization[7:].strip()

        secure_sessions.delete(
            token
        )

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })
