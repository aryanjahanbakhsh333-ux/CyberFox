from __future__ import annotations

import os

import stripe

from flask import (
    Blueprint,
    jsonify,
    request,
)

from database import db
from models import User, Payment
from final_security_system import get_secure_session
from owner_service import is_owner


owner_finance_api = Blueprint(
    "owner_finance_api",
    __name__,
    url_prefix="/api/owner/finance",
)


stripe.api_key = os.getenv(
    "STRIPE_SECRET_KEY",
    "",
).strip()


def _current_user():

    authorization = request.headers.get(
        "Authorization",
        "",
    )

    if not authorization.startswith(
        "Bearer "
    ):
        return None

    token = authorization[
        len("Bearer "):
    ].strip()

    if not token:
        return None

    session = get_secure_session(
        token
    )

    if not session:
        return None

    user_id = session.get(
        "user_id"
    )

    if not user_id:
        return None

    return User.query.get(
        user_id
    )


def _require_owner():

    user = _current_user()

    if not user:

        return None, (
            jsonify({
                "success": False,
                "error": (
                    "Authentication required."
                ),
            }),
            401,
        )

    if not is_owner(user):

        return None, (
            jsonify({
                "success": False,
                "error": (
                    "Owner access required."
                ),
            }),
            403,
        )

    return user, None


def _stripe_ready():

    return bool(
        stripe.api_key
    )


# ============================================================
# OWNER FINANCIAL SUMMARY
# ============================================================

@owner_finance_api.get(
    "/summary"
)
def finance_summary():

    _, error = _require_owner()

    if error:
        return error

    payments = Payment.query.filter_by(
        status="paid"
    ).all()

    totals = {}

    for payment in payments:

        currency = (
            payment.currency
            or "USD"
        ).upper()

        totals[currency] = (
            totals.get(currency, 0.0)
            + float(
                payment.amount or 0
            )
        )

    return jsonify({
        "success": True,
        "payment_count": len(
            payments
        ),
        "revenue_by_currency": totals,
    })


# ============================================================
# STRIPE ACCOUNT BALANCE
# ============================================================

@owner_finance_api.get(
    "/stripe/balance"
)
def stripe_balance():

    _, error = _require_owner()

    if error:
        return error

    if not _stripe_ready():

        return jsonify({
            "success": False,
            "error": (
                "Stripe is not configured."
            ),
        }), 503

    try:

        balance = stripe.Balance.retrieve()

        def normalize(items):

            result = []

            for item in (
                items or []
            ):

                result.append({
                    "amount": (
                        float(
                            item.get(
                                "amount",
                                0,
                            )
                        ) / 100
                    ),
                    "currency": (
                        item.get(
                            "currency",
                            "usd",
                        ).upper()
                    ),
                })

            return result

        return jsonify({
            "success": True,
            "livemode": bool(
                balance.get(
                    "livemode",
                    False,
                )
            ),
            "available": normalize(
                balance.get(
                    "available"
                )
            ),
            "pending": normalize(
                balance.get(
                    "pending"
                )
            ),
        })

    except Exception:

        return jsonify({
            "success": False,
            "error": (
                "Unable to retrieve "
                "Stripe balance."
            ),
        }), 502


# ============================================================
# STRIPE PAYOUTS
# ============================================================

@owner_finance_api.get(
    "/stripe/payouts"
)
def stripe_payouts():

    _, error = _require_owner()

    if error:
        return error

    if not _stripe_ready():

        return jsonify({
            "success": False,
            "error": (
                "Stripe is not configured."
            ),
        }), 503

    try:

        payouts = stripe.Payout.list(
            limit=20
        )

        result = []

        for payout in payouts.data:

            result.append({
                "id": payout.get(
                    "id"
                ),
                "amount": (
                    float(
                        payout.get(
                            "amount",
                            0,
                        )
                    ) / 100
                ),
                "currency": (
                    payout.get(
                        "currency",
                        "usd",
                    ).upper()
                ),
                "status": payout.get(
                    "status"
                ),
                "arrival_date": payout.get(
                    "arrival_date"
                ),
                "created": payout.get(
                    "created"
                ),
            })

        return jsonify({
            "success": True,
            "payouts": result,
        })

    except Exception:

        return jsonify({
            "success": False,
            "error": (
                "Unable to retrieve "
                "Stripe payouts."
            ),
        }), 502


# ============================================================
# FINANCE SECURITY STATUS
# ============================================================

@owner_finance_api.get(
    "/status"
)
def finance_status():

    _, error = _require_owner()

    if error:
        return error

    return jsonify({
        "success": True,
        "provider": "stripe",
        "stripe_configured": (
            _stripe_ready()
        ),

        # CyberFox intentionally does
        # NOT store raw card data.
        "raw_card_storage": False,

        # CyberFox intentionally does
        # NOT store raw bank credentials.
        "raw_bank_credentials_storage": False,

        # Stripe remains the payment processor.
        "payment_processor": "stripe",
    })


def register_owner_finance(
    app,
):
    app.register_blueprint(
        owner_finance_api
    )
