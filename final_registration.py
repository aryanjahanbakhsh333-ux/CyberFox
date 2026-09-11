def register_final_modules(app):
    from final_security_api import (
        final_security_api
    )

    from defense_api_v2 import (
        defense_api_v2
    )

    from security_report_api import (
        security_report_api
    )

    app.register_blueprint(
        final_security_api
    )

    app.register_blueprint(
        defense_api_v2
    )

    app.register_blueprint(
        security_report_api
    )

    return app
