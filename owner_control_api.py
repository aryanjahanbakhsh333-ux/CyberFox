from flask import (
    Blueprint,
    jsonify,
    request
)

from owner_control_service import (
    get_owner_overview,
    verify_owner
)

from subscription_guard import (
    get_current_user
)


owner_control_api = Blueprint(
    "owner_control_api",
    __name__,
    url_prefix="/api/owner-control"
)


@owner_control_api.get("/verify")
def verify():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if not verify_owner(user):
        return jsonify({
            "success": False,
            "error": "Owner access required."
        }), 403

    return jsonify({
        "success": True,
        **get_owner_overview(user)
    })


@owner_control_api.get("/user/<int:user_id>")
def user_info(user_id):
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if not verify_owner(user):
        return jsonify({
            "success": False,
            "error": "Owner access required."
        }), 403

    from owner_control_service import find_user

    target = find_user(user_id)

    if not target:
        return jsonify({
            "success": False,
            "error": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": target.id,
            "email": target.email,
            "plan": target.plan,
            "role": target.role,
            "is_active": target.is_active,
            "created_at":
                target.created_at.isoformat()
                if target.created_at
                else None,
            "last_login":
                target.last_login.isoformat()
                if target.last_login
                else None
        }
    })
