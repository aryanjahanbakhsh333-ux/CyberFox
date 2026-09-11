from datetime import datetime

from database import db
from models import SecurityEvent


def write_audit_event(
    user_id,
    event_type,
    description,
    severity="info"
):
    event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        description=description,
        severity=severity,
        created_at=datetime.utcnow()
    )

    db.session.add(event)
    db.session.commit()

    return event


def serialize_event(event):
    return {
        "id": event.id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "description": event.description,
        "severity": event.severity,
        "created_at":
            event.created_at.isoformat()
            if event.created_at
            else None
    }
