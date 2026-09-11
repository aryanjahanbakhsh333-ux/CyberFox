from database import db
from models import User, Payment


def handle_checkout_completed(event):
    session = event.get("data", {}).get(
        "object",
        {}
    )

    metadata = session.get(
        "metadata",
        {}
    )

    user_id = metadata.get(
        "user_id"
    )

    if not user_id:
        return False

    user = User.query.get(
        int(user_id)
    )

    if not user:
        return False

    transaction_id = session.get(
        "id"
    )

    existing_payment = Payment.query.filter_by(
        transaction_id=transaction_id
    ).first()

    if existing_payment:
        return True

    user.plan = "pro"

    payment = Payment(
        user_id=user.id,
        provider="stripe",
        transaction_id=transaction_id,
        amount=0.0,
        currency="USD",
        status="paid"
    )

    db.session.add(payment)

    db.session.commit()

    return True


def handle_subscription_deleted(event):
    subscription = event.get(
        "data",
        {}
    ).get(
        "object",
        {}
    )

    metadata = subscription.get(
        "metadata",
        {}
    )

    user_id = metadata.get(
        "user_id"
    )

    if not user_id:
        return False

    user = User.query.get(
        int(user_id)
    )

    if not user:
        return False

    user.plan = "free"

    db.session.commit()

    return True
