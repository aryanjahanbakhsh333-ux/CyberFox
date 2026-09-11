from datetime import datetime

from database import db


class Subscription(db.Model):

    __tablename__ = "subscriptions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    provider = db.Column(
        db.String(50),
        nullable=False,
        default="stripe"
    )

    customer_id = db.Column(
        db.String(255),
        nullable=True,
        index=True
    )

    subscription_id = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    price_id = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    current_period_start = db.Column(
        db.DateTime,
        nullable=True
    )

    current_period_end = db.Column(
        db.DateTime,
        nullable=True
    )

    cancel_at_period_end = db.Column(
        db.Boolean,
        nullable=False,
        default=False
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
