from functools import wraps

from flask import jsonify


def require_role(required_role):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            user = kwargs.get(
                "current_user"
            )

            if not user:
                return jsonify({
                    "success": False,
                    "error": "Authentication required."
                }), 401

            if user.role != required_role:
                return jsonify({
                    "success": False,
                    "error": "Insufficient permissions."
                }), 403

            return function(
                *args,
                **kwargs
            )

        return wrapper

    return decorator
