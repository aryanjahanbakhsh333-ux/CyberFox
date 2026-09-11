from flask import Flask

from config import Config
from database import init_database


def create_final_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_database(app)

    try:
        from api_routes import register_api_routes
        register_api_routes(app)
    except ImportError:
        pass

    try:
        from integrate_final_system import (
            integrate_final_system
        )
        integrate_final_system(app)
    except ImportError:
        pass

    try:
        from recovery_routes_registration import (
            register_recovery_routes
        )
        register_recovery_routes(app)
    except ImportError:
        pass

    return app
