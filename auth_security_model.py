from datetime import datetime

from database import db


class AuthSecurity(db.Model):
    __tablename__ = "auth_security"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    totp_enabled = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    totp_secret = db.Column(
        db.String(128),
        nullable=True
    )

    recovery_codes = db.Column(
        db.Text,
        nullable=True
    )

    last_2fa_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
