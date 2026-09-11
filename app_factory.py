from flask import Flask

from config import Config
from database import init_database

from api_auth import auth_api
from owner_api import owner_api


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_database(app)

    app.register_blueprint(auth_api)
    app.register_blueprint(owner_api)

    return app
