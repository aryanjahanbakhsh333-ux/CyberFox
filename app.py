from app_factory import create_app

from security_api import security_api
from plan_api import plan_api
from event_api import event_api
from health_api import health_api


app = create_app()

app.register_blueprint(
    security_api
)

app.register_blueprint(
    plan_api
)

app.register_blueprint(
    event_api
)

app.register_blueprint(
    health_api
)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
