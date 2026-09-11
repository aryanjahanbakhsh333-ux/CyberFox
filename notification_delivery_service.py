from datetime import datetime

from database import db
from notification_delivery_model import (
    NotificationDelivery
)


def create_delivery(
    user_id,
    channel,
    subject
):
    delivery = NotificationDelivery(
        user_id=user_id,
        channel=channel,
        subject=subject,
        status="pending"
    )

    db.session.add(delivery)
    db.session.commit()

    return delivery


def mark_sent(delivery):
    delivery.status = "sent"
    delivery.sent_at = datetime.utcnow()

    db.session.commit()

    return delivery


def mark_failed(delivery):
    delivery.status = "failed"

    db.session.commit()

    return delivery
