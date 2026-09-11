from database import db
from models import Payment


def create_payment(
    user_id,
    provider,
    amount,
    currency="USD"
):
    payment = Payment(
        user_id=user_id,
        provider=provider,
        amount=amount,
        currency=currency,
        status="pending"
    )

    db.session.add(payment)
    db.session.commit()

    return payment


def update_payment_status(
    payment,
    status,
    transaction_id=None
):
    payment.status = status

    if transaction_id:
        payment.transaction_id = transaction_id

    db.session.commit()

    return payment
