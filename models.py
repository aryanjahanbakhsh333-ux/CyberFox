from datetime import datetime

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    plan = db.Column(
        db.String(20),
        nullable=False,
        default="free"
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )


class SecurityEvent(db.Model):
    __tablename__ = "security_events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    event_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    severity = db.Column(
        db.String(20),
        default="info"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    provider = db.Column(
        db.String(50),
        nullable=False
    )

    transaction_id = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    currency = db.Column(
        db.String(10),
        default="USD"
    )

    status = db.Column(
        db.String(30),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
