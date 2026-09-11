def register_final_routes(app):
    from billing_state_api import (
        billing_state_api
    )

    from owner_control_api import (
        owner_control_api
    )

    from security_audit_api import (
        security_audit_api
    )

    from feature_registry_api import (
        feature_registry_api
    )

    app.register_blueprint(
        billing_state_api
    )

    app.register_blueprint(
        owner_control_api
    )

    app.register_blueprint(
        security_audit_api
    )

    app.register_blueprint(
        feature_registry_api
    )

    return app
