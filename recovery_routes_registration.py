def register_recovery_routes(app):
    from recovery_api import recovery_api

    from production_runtime_api import (
        production_runtime_api
    )

    app.register_blueprint(
        recovery_api
    )

    app.register_blueprint(
        production_runtime_api
    )

    return app
