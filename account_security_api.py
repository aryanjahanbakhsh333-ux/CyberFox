from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User
from session_service import get_session

from account_security_service import (
    get_security_record
)


account_security_api = Blueprint(
    "account_security_api",
    __name__,
    url_prefix="/api/account-security"
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


@account_security_api.get("/")
def security_status():

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
        "security": {
            "email_verified":
                record.email_verified,
            "two_factor_enabled":
                record.two_factor_enabled
        }
    })
