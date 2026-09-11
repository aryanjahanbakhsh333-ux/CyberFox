from flask import (
    Blueprint,
    jsonify,
    request
)

from models import User
from session_service import get_session
from payment_config import PaymentConfig
from stripe_provider import StripeProvider
from payment_provider import PaymentProviderError
from payment_webhook_service import (
    handle_checkout_completed,
    handle_subscription_deleted
)


payment_routes = Blueprint(
    "payment_routes",
    __name__,
    url_prefix="/api/payments"
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


@payment_routes.post("/checkout")
def create_checkout():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    if user.plan == "pro":
        return jsonify({
            "success": False,
            "error": "User is already Pro."
        }), 409

    try:
        provider = StripeProvider()

        session = provider.create_checkout_session(
            user=user,
            success_url=PaymentConfig.SUCCESS_URL,
            cancel_url=PaymentConfig.CANCEL_URL
        )

        return jsonify({
            "success": True,
            "checkout_url": session["url"],
            "session_id": session["id"]
        })

    except PaymentProviderError as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 503


@payment_routes.post("/webhook")
def payment_webhook():
    payload = request.get_data()

    signature = request.headers.get(
        "Stripe-Signature",
        ""
    )

    try:
        provider = StripeProvider()

        event = provider.verify_webhook(
            payload,
            signature
        )

        event_type = event.get(
            "type"
        )

        if event_type == (
            "checkout.session.completed"
        ):
            handle_checkout_completed(
                event
            )

        elif event_type == (
            "customer.subscription.deleted"
        ):
            handle_subscription_deleted(
                event
            )

        return jsonify({
            "success": True
        })

    except PaymentProviderError as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400
