from datetime import datetime

from models import Payment


def get_billing_state(user):
    payments = (
        Payment.query
        .filter_by(user_id=user.id)
        .order_by(
            Payment.created_at.desc()
        )
        .all()
    )

    latest = payments[0] if payments else None

    return {
        "plan": user.plan,
        "is_pro": user.plan == "pro",
        "latest_payment": (
            {
                "id": latest.id,
                "provider": latest.provider,
                "transaction_id":
                    latest.transaction_id,
                "amount": latest.amount,
                "currency": latest.currency,
                "status": latest.status,
                "created_at":
                    latest.created_at.isoformat()
                    if latest.created_at
                    else None
            }
            if latest
            else None
        )
    }
