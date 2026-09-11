from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User
from session_service import get_session

from two_factor_service import (
    create_2fa_code,
    verify_2fa_code
)

from account_security_service import (
    enable_2fa,
    disable_2fa,
    get_security_record
)


two_factor_api = Blueprint(
    "two_factor_api",
    __name__,
    url_prefix="/api/2fa"
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


@two_factor_api.get("/status")
def status():

    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    record = get_security_record(
        user.id
    )

    return jsonify({
        "success": True,
        "enabled":
            record.two_factor_enabled,
        "email_verified":
            record.email_verified
    })


@two_factor_api.post("/send")
def send():

    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    code = create_2fa_code(
        user.id
    )

    return jsonify({
        "success": True,
        "message": (
            "Two-factor verification code "
            "generated."
        ),
        "delivery": "email"
    })


@two_factor_api.post("/verify")
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

    if not verify_2fa_code(
        user.id,
        code
    ):
        return jsonify({
            "success": False,
            "error": "Invalid or expired code."
        }), 400

    enable_2fa(
        user.id
    )

    return jsonify({
        "success": True,
        "message": (
            "Two-factor authentication enabled."
        )
    })


@two_factor_api.post("/disable")
def disable():

    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    disable_2fa(
        user.id
    )

    return jsonify({
        "success": True,
        "message": (
            "Two-factor authentication disabled."
        )
    })
