from datetime import datetime

from database import db


class NotificationDelivery(db.Model):
    __tablename__ = "notification_deliveries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    channel = db.Column(
        db.String(30),
        nullable=False
    )

    subject = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sent_at = db.Column(
        db.DateTime,
        nullable=True
    )
