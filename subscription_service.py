from datetime import datetime

from database import db
from models import Payment


def activate_pro_subscription(
    user,
    provider,
    transaction_id,
    amount=0.0,
    currency="USD"
):
    if not user:
        return None

    user.plan = "pro"

    payment = Payment(
        user_id=user.id,
        provider=provider,
        transaction_id=transaction_id,
        amount=amount,
        currency=currency,
        status="paid",
        created_at=datetime.utcnow()
    )

    db.session.add(payment)
    db.session.commit()

    return payment


def deactivate_pro_subscription(user):
    if not user:
        return False

    user.plan = "free"

    db.session.commit()

    return True
