from flask import (
    Blueprint,
    jsonify
)

from subscription_guard import (
    get_current_user
)

from models import SecurityEvent

from security_audit_log import (
    serialize_event
)


security_audit_api = Blueprint(
    "security_audit_api",
    __name__,
    url_prefix="/api/security-audit"
)


@security_audit_api.get("/")
def events():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    events = (
        SecurityEvent.query
        .filter_by(user_id=user.id)
        .order_by(
            SecurityEvent.created_at.desc()
        )
        .limit(100)
        .all()
    )

    return jsonify({
        "success": True,
        "events": [
            serialize_event(event)
            for event in events
        ]
    })
