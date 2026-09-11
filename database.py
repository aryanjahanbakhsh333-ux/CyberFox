from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_database(app):
    database_url = app.config.get(
        "DATABASE_URL",
        "sqlite:///security_platform.db"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
