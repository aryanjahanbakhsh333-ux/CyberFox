from functools import wraps

from flask import jsonify


def pro_required(function):
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

        if user.plan != "pro":
            return jsonify({
                "success": False,
                "error": "Pro plan required.",
                "upgrade_required": True
            }), 403

        return function(
            *args,
            **kwargs
        )

    return wrapper
