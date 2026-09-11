from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User, Payment
from owner_service import is_owner
from session_service import get_session


owner_billing_api = Blueprint(
    "owner_billing_api",
    __name__,
    url_prefix="/api/owner/billing"
)


def get_current_user():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith(
        "Bearer "
    ):
        return None

    token = authorization[7:].strip()

    session = get_session(token)

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@owner_billing_api.get("/summary")
def billing_summary():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if not is_owner(user):
        return jsonify({
            "success": False,
            "error": "Owner access required."
        }), 403

    total_payments = Payment.query.filter_by(
        status="paid"
    ).count()

    total_revenue = 0.0

    payments = Payment.query.filter_by(
        status="paid"
    ).all()

    for payment in payments:
        total_revenue += float(
            payment.amount or 0
        )

    return jsonify({
        "success": True,
        "payments": total_payments,
        "revenue": total_revenue
    })
