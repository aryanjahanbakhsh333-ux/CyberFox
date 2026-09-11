from datetime import datetime

from database import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    action = db.Column(
        db.String(100),
        nullable=False
    )

    resource = db.Column(
        db.String(255),
        nullable=True
    )

    result = db.Column(
        db.String(50),
        nullable=False,
        default="success"
    )

    ip_address = db.Column(
        db.String(64),
        nullable=True
    )

    user_agent = db.Column(
        db.Text,
        nullable=True
    )

    details = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
