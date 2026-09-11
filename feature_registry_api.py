from flask import (
    Blueprint,
    jsonify
)

from subscription_guard import (
    get_current_user
)

from pro_feature_registry import (
    list_features
)


feature_registry_api = Blueprint(
    "feature_registry_api",
    __name__,
    url_prefix="/api/features"
)


@feature_registry_api.get("/")
def features():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "plan": user.plan,
        "features":
            list_features(user.plan)
    })
