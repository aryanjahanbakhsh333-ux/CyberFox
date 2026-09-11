from datetime import datetime

from database import db
from webhook_event_model import WebhookEvent


def already_processed(event_id):
    event = WebhookEvent.query.filter_by(
        event_id=event_id
    ).first()

    return bool(
        event and event.processed
    )


def register_webhook(
    provider,
    event_id,
    event_type
):
    existing = WebhookEvent.query.filter_by(
        event_id=event_id
    ).first()

    if existing:
        return existing, False

    event = WebhookEvent(
        provider=provider,
        event_id=event_id,
        event_type=event_type,
        processed=False
    )

    db.session.add(event)
    db.session.commit()

    return event, True


def mark_webhook_processed(event):
    event.processed = True
    event.processed_at = datetime.utcnow()

    db.session.commit()
