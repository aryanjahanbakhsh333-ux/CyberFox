from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User
from session_service import get_session

from verification_service import (
    create_verification_code,
    verify_code
)

from account_security_service import (
    verify_email
)


verification_api = Blueprint(
    "verification_api",
    __name__,
    url_prefix="/api/verification"
)


def get_current_user():

    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith(
        "Bearer "
    ):
        return None

    token = authorization[7:].strip()

    session = get_session(
        token
    )

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@verification_api.post("/send")
def send_code():

    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    code = create_verification_code(
        user.id
    )

    # Email provider will deliver
    # the code in production.

    return jsonify({
        "success": True,
        "message": (
            "Verification code generated."
        ),
        "delivery": "email"
    })


@verification_api.post("/verify")
def verify():

    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    code = data.get(
        "code",
        ""
    )

    if not verify_code(
        user.id,
        code
    ):
        return jsonify({
            "success": False,
            "error": "Invalid or expired code."
        }), 400

    verify_email(
        user.id
    )

    return jsonify({
        "success": True,
        "message": "Email verified successfully."
    })
