from flask import (
    Blueprint,
    jsonify,
    request
)

from password_reset_service import (
    create_reset_code,
    reset_password
)


password_reset_api = Blueprint(
    "password_reset_api",
    __name__,
    url_prefix="/api/password-reset"
)


@password_reset_api.post("/request")
def request_reset():

    data = request.get_json(
        silent=True
    ) or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    if not email:
        return jsonify({
            "success": False,
            "error": "Email is required."
        }), 400

    code = create_reset_code(
        email
    )

    # For security, do not reveal
    # whether an account exists.

    return jsonify({
        "success": True,
        "message": (
            "If the account exists, "
            "a reset code will be sent."
        )
    })


@password_reset_api.post("/confirm")
def confirm_reset():

    data = request.get_json(
        silent=True
    ) or {}

    user_id = data.get(
        "user_id"
    )

    code = data.get(
        "code",
        ""
    )

    new_password = data.get(
        "new_password",
        ""
    )

    if not user_id or not code:
        return jsonify({
            "success": False,
            "error": "Reset information is required."
        }), 400

    success = reset_password(
        user_id,
        code,
        new_password
    )

    if not success:
        return jsonify({
            "success": False,
            "error": (
                "Invalid reset request."
            )
        }), 400

    return jsonify({
        "success": True,
        "message": (
            "Password reset successfully."
        )
    })
