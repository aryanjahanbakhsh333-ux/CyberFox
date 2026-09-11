from datetime import datetime

from database import db


class Threat(db.Model):
    __tablename__ = "threats"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    threat_type = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    severity = db.Column(
        db.String(20),
        nullable=False,
        default="low"
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="detected"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
