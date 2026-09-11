from flask import (
    Blueprint,
    jsonify
)

from subscription_guard import (
    get_current_user
)

from billing_state_service import (
    get_billing_state
)


billing_state_api = Blueprint(
    "billing_state_api",
    __name__,
    url_prefix="/api/billing"
)


@billing_state_api.get("/state")
def state():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        **get_billing_state(user)
    })
