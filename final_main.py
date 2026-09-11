import os

from flask import Flask

from config import Config
from database import init_database


def create_application():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_database(app)

    from api_routes import register_api_routes

    register_api_routes(app)

    try:
        from ai_routes_registration import (
            register_ai_routes
        )

        register_ai_routes(app)
    except ImportError:
        pass

    try:
        from recovery_routes_registration import (
            register_recovery_routes
        )

        register_recovery_routes(app)
    except ImportError:
        pass

    from final_route_registration import (
        register_final_routes
    )

    register_final_routes(app)

    return app


app = create_application()


if __name__ == "__main__":
    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
