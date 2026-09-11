import os
import stripe

from flask import Blueprint, jsonify, request

from database import db
from models import User, Payment


payment_api = Blueprint(
    "real_payment_api",
    __name__,
    url_prefix="/api/payment"
)


stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

PRO_PRICE_CENTS = int(
    os.getenv("PRO_PRICE_CENTS", "1999")
)

PRO_CURRENCY = os.getenv(
    "PRO_CURRENCY",
    "usd"
)

STRIPE_PRICE_ID = os.getenv(
    "STRIPE_PRICE_ID",
    ""
)

PUBLIC_URL = os.getenv(
    "PUBLIC_URL",
    ""
)

WEBHOOK_SECRET = os.getenv(
    "STRIPE_WEBHOOK_SECRET",
    ""
)


def get_user_from_token():

    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[7:].strip()

    # Connect this function to your project's
    # canonical secure-session implementation.
    from final_security_system import (
        get_secure_session
    )

    session = get_secure_session(token)

    if not session:
        return None

    return User.query.get(
        session["user_id"]
    )


def stripe_ready():

    return bool(
        stripe.api_key
        and STRIPE_PRICE_ID
        and PUBLIC_URL
    )


@payment_api.get("/status")
def payment_status():

    return jsonify({
        "success": True,
        "configured": stripe_ready(),
        "currency": PRO_CURRENCY,
        "pro_price_cents": PRO_PRICE_CENTS
    })


@payment_api.post("/checkout")
def create_checkout():

    user = get_user_from_token()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if user.plan == "pro":
        return jsonify({
            "success": False,
            "error": "User already has Pro."
        }), 409

    if not stripe_ready():
        return jsonify({
            "success": False,
            "error": "Payment system is not configured."
        }), 503

    try:

        session = stripe.checkout.Session.create(

            mode="subscription",

            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1
                }
            ],

            customer_email=user.email,

            client_reference_id=str(
                user.id
            ),

            metadata={
                "user_id": str(user.id),
                "plan": "pro"
            },

            success_url=(
                PUBLIC_URL
                + "/payment-success"
                + "?session_id={CHECKOUT_SESSION_ID}"
            ),

            cancel_url=(
                PUBLIC_URL
                + "/payment-cancelled"
            )
        )

        return jsonify({
            "success": True,
            "checkout_url": session.url,
            "session_id": session.id
        })

    except Exception:

        return jsonify({
            "success": False,
            "error": "Unable to create checkout session."
        }), 500


@payment_api.post("/webhook")
def stripe_webhook():

    if not WEBHOOK_SECRET:
        return jsonify({
            "success": False,
            "error": "Webhook secret is not configured."
        }), 503

    payload = request.get_data()
    signature = request.headers.get(
        "Stripe-Signature",
        ""
    )

    try:

        event = stripe.Webhook.construct_event(
            payload,
            signature,
            WEBHOOK_SECRET
        )

    except ValueError:

        return jsonify({
            "success": False,
            "error": "Invalid webhook payload."
        }), 400

    except stripe.error.SignatureVerificationError:

        return jsonify({
            "success": False,
            "error": "Invalid webhook signature."
        }), 400

    event_type = event["type"]

    if event_type == "checkout.session.completed":

        session = event["data"]["object"]

        user_id = (
            session.get("metadata", {})
            .get("user_id")
        )

        subscription_id = (
            session.get("subscription")
        )

        checkout_id = session.get("id")

        if not user_id:
            return jsonify({
                "success": False,
                "error": "Missing user reference."
            }), 400

        user = User.query.get(
            int(user_id)
        )

        if not user:
            return jsonify({
                "success": False,
                "error": "User not found."
            }), 404

        existing = (
            Payment.query
            .filter_by(
                transaction_id=checkout_id
            )
            .first()
        )

        if existing:
            return jsonify({
                "success": True,
                "duplicate": True
            })

        user.plan = "pro"

        payment = Payment(
            user_id=user.id,
            provider="stripe",
            transaction_id=checkout_id,
            amount=PRO_PRICE_CENTS / 100,
            currency=PRO_CURRENCY,
            status="paid"
        )

        db.session.add(payment)
        db.session.commit()

        return jsonify({
            "success": True,
            "processed": True,
            "subscription_id": subscription_id
        })

    if event_type in {
        "customer.subscription.deleted",
        "customer.subscription.paused"
    }:

        subscription = event["data"]["object"]

        customer_id = subscription.get(
            "customer"
        )

        # Subscription/customer mapping should be
        # stored in your production database.
        # Never downgrade users based only on
        # unverified client-side information.

        return jsonify({
            "success": True,
            "subscription_event": event_type,
            "customer": customer_id
        })

    return jsonify({
        "success": True,
        "received": True,
        "event": event_type
    })


def register_real_payment(app):

    app.register_blueprint(
        payment_api
    )
