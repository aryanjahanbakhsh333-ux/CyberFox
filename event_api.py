from flask import Blueprint, jsonify, request

from models import SecurityEvent, User
from session_service import get_session


event_api = Blueprint(
    "event_api",
    __name__,
    url_prefix="/api/events"
)


def get_current_user():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return None

    return User.query.get(session["user_id"])


@event_api.get("/")
def get_events():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    events = SecurityEvent.query.filter_by(
        user_id=user.id
    ).order_by(
        SecurityEvent.created_at.desc()
    ).limit(100).all()

    return jsonify({
        "success": True,
        "events": [
            {
                "id": event.id,
                "type": event.event_type,
                "description": event.description,
                "severity": event.severity,
                "created_at": event.created_at.isoformat()
            }
            for event in events
        ]
    })
