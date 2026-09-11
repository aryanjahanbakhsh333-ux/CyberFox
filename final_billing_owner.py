import os
from functools import wraps

from flask import Blueprint, jsonify, request

from database import db
from models import User, Payment, SecurityEvent

from final_security_system import current_user


billing_owner_api = Blueprint(
    "billing_owner_api",
    __name__,
    url_prefix="/api"
)


# --------------------------------------------------
# PLANS
# --------------------------------------------------

PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "currency": "USD"
    },
    "pro": {
        "name": "Pro",
        "price": 19.99,
        "currency": "USD"
    }
}


def pro_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        if user.plan != "pro":
            return jsonify({
                "success": False,
                "error": "Pro subscription required."
            }), 403

        return function(user, *args, **kwargs)

    return wrapper


def owner_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        owner_email = os.getenv(
            "OWNER_EMAIL",
            ""
        ).strip().lower()

        if (
            user.role != "owner"
            or not owner_email
            or user.email.lower() != owner_email
        ):
            return jsonify({
                "success": False,
                "error": "Owner access required."
            }), 403

        return function(user, *args, **kwargs)

    return wrapper


# --------------------------------------------------
# BILLING
# --------------------------------------------------

@billing_owner_api.get("/billing/plans")
def plans():

    return jsonify({
        "success": True,
        "plans": PLANS
    })


@billing_owner_api.get("/billing/state")
def billing_state():

    user = current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    payment = (
        Payment.query
        .filter_by(user_id=user.id)
        .order_by(Payment.created_at.desc())
        .first()
    )

    return jsonify({
        "success": True,
        "plan": user.plan,
        "is_pro": user.plan == "pro",
        "latest_payment": (
            {
                "provider": payment.provider,
                "transaction_id": payment.transaction_id,
                "amount": payment.amount,
                "currency": payment.currency,
                "status": payment.status
            }
            if payment
            else None
        )
    })


# --------------------------------------------------
# PAYMENT CREATION
# --------------------------------------------------

@billing_owner_api.post("/billing/checkout")
def checkout():

    user = current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    # The amount is NEVER accepted from the client.
    plan = "pro"
    amount = PLANS[plan]["price"]
    currency = PLANS[plan]["currency"]

    provider_key = os.getenv(
        "PAYMENT_SECRET_KEY",
        ""
    )

    if not provider_key:
        return jsonify({
            "success": False,
            "error": (
                "Payment provider is not configured."
            )
        }), 503

    # The actual Stripe Checkout Session should be
    # created by the configured payment provider.
    return jsonify({
        "success": True,
        "provider": "stripe",
        "plan": plan,
        "amount": amount,
        "currency": currency,
        "message": (
            "Payment provider is ready for Checkout integration."
        )
    })


# --------------------------------------------------
# OWNER ROOM
# --------------------------------------------------

@billing_owner_api.get("/owner/overview")
@owner_required
def owner_overview(user):

    users = User.query.count()

    pro_users = User.query.filter_by(
        plan="pro"
    ).count()

    payments = Payment.query.count()

    events = SecurityEvent.query.count()

    return jsonify({
        "success": True,
        "owner": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        },
        "statistics": {
            "users": users,
            "pro_users": pro_users,
            "payments": payments,
            "security_events": events
        }
    })


@billing_owner_api.get("/owner/users")
@owner_required
def owner_users(user):

    rows = (
        User.query
        .order_by(User.created_at.desc())
        .limit(500)
        .all()
    )

    return jsonify({
        "success": True,
        "users": [
            {
                "id": item.id,
                "email": item.email,
                "plan": item.plan,
                "role": item.role,
                "active": item.is_active,
                "created_at": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                )
            }
            for item in rows
        ]
    })


@billing_owner_api.get("/owner/payments")
@owner_required
def owner_payments(user):

    rows = (
        Payment.query
        .order_by(Payment.created_at.desc())
        .limit(500)
        .all()
    )

    return jsonify({
        "success": True,
        "payments": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "provider": item.provider,
                "transaction_id": item.transaction_id,
                "amount": item.amount,
                "currency": item.currency,
                "status": item.status,
                "created_at": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                )
            }
            for item in rows
        ]
    })


@billing_owner_api.get("/owner/security-events")
@owner_required
def owner_security_events(user):

    rows = (
        SecurityEvent.query
        .order_by(SecurityEvent.created_at.desc())
        .limit(500)
        .all()
    )

    return jsonify({
        "success": True,
        "events": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "type": item.event_type,
                "description": item.description,
                "severity": item.severity,
                "created_at": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                )
            }
            for item in rows
        ]
    })


def register_billing_owner(app):
    app.register_blueprint(billing_owner_api)
