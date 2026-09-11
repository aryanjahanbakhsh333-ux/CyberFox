from datetime import datetime

from database import db


class ManagedDevice(db.Model):
    __tablename__ = "managed_devices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    device_id = db.Column(
        db.String(255),
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    platform = db.Column(
        db.String(50),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="unknown",
        nullable=False
    )

    last_seen = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
