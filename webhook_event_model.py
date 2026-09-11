from datetime import datetime

from database import db


class WebhookEvent(db.Model):
    __tablename__ = "webhook_events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    provider = db.Column(
        db.String(50),
        nullable=False
    )

    event_id = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    event_type = db.Column(
        db.String(100),
        nullable=False
    )

    processed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    processed_at = db.Column(
        db.DateTime,
        nullable=True
    )
