import os

from flask import Flask, jsonify

from config import Config
from database import init_database


def create_final_application():

    app = Flask(__name__)

    app.config.from_object(Config)

    # --------------------------------------------------
    # CORE DATABASE
    # --------------------------------------------------

    init_database(app)

    # --------------------------------------------------
    # EXISTING SYSTEM ROUTES
    # --------------------------------------------------

    try:
        from api_routes import register_api_routes

        register_api_routes(app)
    except ImportError:
        pass

    # --------------------------------------------------
    # FINAL SECURITY SYSTEM
    # --------------------------------------------------

    from final_security_system import (
        register_security_final
    )

    register_security_final(app)

    # --------------------------------------------------
    # FINAL AI + RECOVERY
    # --------------------------------------------------

    from final_ai_recovery import (
        register_ai_recovery
    )

    register_ai_recovery(app)

    # --------------------------------------------------
    # FINAL BILLING + OWNER
    # --------------------------------------------------

    from final_billing_owner import (
        register_billing_owner
    )

    register_billing_owner(app)

    # --------------------------------------------------
    # HEALTH
    # --------------------------------------------------

    @app.get("/api/final-health")
    def final_health():

        return jsonify({
            "success": True,
            "status": "online",
            "application": (
                "Cybersecurity AI Platform"
            ),
            "version": "final",
            "systems": {
                "authentication": True,
                "security_engine": True,
                "ai_security": True,
                "threat_analysis": True,
                "recovery": True,
                "billing": True,
                "owner_room": True,
                "audit_logs": True,
                "pro_access": True
            }
        })

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "error": "Resource not found."
        }), 404

    @app.errorhandler(500)
    def server_error(error):

        return jsonify({
            "success": False,
            "error": "Internal server error."
        }), 500

    return app


app = create_final_application()


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
