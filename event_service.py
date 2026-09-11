from database import db
from models import SecurityEvent


def record_event(
    event_type,
    description,
    severity="info",
    user_id=None
):
    event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        description=description,
        severity=severity
    )

    db.session.add(event)
    db.session.commit()

    return event
