from functools import wraps

from flask import request, jsonify


def get_auth_token():
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return None

    return authorization[7:].strip()


def require_authentication():
    token = get_auth_token()

    if not token:
        return None, (
            jsonify({
                "success": False,
                "error": "Authentication required."
            }),
            401
        )

    # Real token validation will be added
    # when the authentication system is implemented.
    return token, None


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token, error = require_authentication()

        if error:
            return error

        return function(*args, **kwargs)

    return wrapper
