from flask import request

from security_headers import (
    apply_security_headers
)

from production_security import (
    validate_production_environment
)


def register_security_middleware(app):

    @app.after_request
    def security_headers(response):

        return apply_security_headers(
            response
        )

    @app.before_request
    def production_check():

        if request.path.startswith(
            "/api/"
        ):
            return None

        return None

    app.config[
        "PRODUCTION_SECURITY"
    ] = validate_production_environment()

    return app
