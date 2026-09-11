from payment_routes import payment_routes
from billing_api import billing_api
from owner_billing_api import owner_billing_api


def register_billing_routes(app):

    app.register_blueprint(
        payment_routes
    )

    app.register_blueprint(
        billing_api
    )

    app.register_blueprint(
        owner_billing_api
    )
