class PaymentProviderError(Exception):
    pass


class PaymentProvider:
    def create_checkout_session(
        self,
        user,
        success_url,
        cancel_url
    ):
        raise NotImplementedError

    def verify_webhook(
        self,
        payload,
        signature
    ):
        raise NotImplementedError
