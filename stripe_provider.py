import os

from payment_provider import PaymentProviderError


class StripeProvider:

    def __init__(self):
        self.secret_key = os.getenv(
            "PAYMENT_SECRET_KEY",
            ""
        )

        self.webhook_secret = os.getenv(
            "PAYMENT_WEBHOOK_SECRET",
            ""
        )

        self.price_id = os.getenv(
            "PRO_PRICE_ID",
            ""
        )

        if not self.secret_key:
            raise PaymentProviderError(
                "Payment provider secret key is not configured."
            )

        if not self.price_id:
            raise PaymentProviderError(
                "Pro price ID is not configured."
            )

        try:
            import stripe
        except ImportError as exc:
            raise PaymentProviderError(
                "Stripe package is not installed."
            ) from exc

        self.stripe = stripe
        self.stripe.api_key = self.secret_key

    def create_checkout_session(
        self,
        user,
        success_url,
        cancel_url
    ):
        if not user:
            raise PaymentProviderError(
                "User is required."
            )

        if not user.email:
            raise PaymentProviderError(
                "User email is required."
            )

        try:
            session = self.stripe.checkout.Session.create(
                mode="subscription",
                line_items=[
                    {
                        "price": self.price_id,
                        "quantity": 1
                    }
                ],
                customer_email=user.email,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": str(user.id)
                }
            )

            return {
                "id": session.id,
                "url": session.url
            }

        except Exception as exc:
            raise PaymentProviderError(
                "Unable to create checkout session."
            ) from exc

    def verify_webhook(
        self,
        payload,
        signature
    ):
        if not self.webhook_secret:
            raise PaymentProviderError(
                "Webhook secret is not configured."
            )

        if not signature:
            raise PaymentProviderError(
                "Webhook signature is missing."
            )

        try:
            event = self.stripe.Webhook.construct_event(
                payload,
                signature,
                self.webhook_secret
            )

            return event

        except Exception as exc:
            raise PaymentProviderError(
                "Invalid webhook signature."
            ) from exc
