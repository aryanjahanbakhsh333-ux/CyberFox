from flask import Blueprint, jsonify, request

from models import User
from payment_service import create_payment
from session_service import get_session


payment_api = Blueprint(
    "payment_api",
    __name__,
    url_prefix="/api/payments"
)


def get_current_user():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


@payment_api.post("/create")
def create():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    amount = data.get("amount", 0)
    currency = data.get(
        "currency",
        "USD"
    )

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "Invalid amount."
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "error": "Amount must be greater than zero."
        }), 400

    payment = create_payment(
        user_id=user.id,
        provider="external",
        amount=amount,
        currency=currency
    )

    return jsonify({
        "success": True,
        "payment_id": payment.id,
        "status": payment.status
    }), 201
