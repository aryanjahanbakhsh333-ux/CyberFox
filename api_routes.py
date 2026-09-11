from flask import Blueprint, jsonify

from ai_api import ai_api
from dashboard_api import dashboard_api
from emergency_api import emergency_api
from event_api import event_api
from health_api import health_api
from notification_api import notification_api
from owner_dashboard_api import owner_dashboard_api
from payment_api import payment_api
from plan_api import plan_api
from recommendation_api import recommendation_api
from risk_api import risk_api
from security_api import security_api
from security_score_api import score_api
from threat_api import threat_api
from user_api import user_api


api_routes = Blueprint(
    "api_routes",
    __name__
)


@api_routes.get("/api")
def api_home():
    return jsonify({
        "success": True,
        "service": "Cybersecurity AI Platform",
        "status": "operational"
    })


def register_api_routes(app):
    app.register_blueprint(ai_api)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(emergency_api)
    app.register_blueprint(event_api)
    app.register_blueprint(health_api)
    app.register_blueprint(notification_api)
    app.register_blueprint(owner_dashboard_api)
    app.register_blueprint(payment_api)
    app.register_blueprint(plan_api)
    app.register_blueprint(recommendation_api)
    app.register_blueprint(risk_api)
    app.register_blueprint(security_api)
    app.register_blueprint(score_api)
    app.register_blueprint(threat_api)
    app.register_blueprint(user_api)
