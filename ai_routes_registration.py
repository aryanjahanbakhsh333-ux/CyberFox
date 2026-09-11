def register_ai_routes(app):
    from ai_final_api import (
        ai_final_api
    )

    from ai_health_api import (
        ai_health_api
    )

    from ai_usage_api import (
        ai_usage_api
    )

    from ai_security_api_v2 import (
        ai_security_api_v2
    )

    from ai_chat_api_v2 import (
        ai_chat_api_v2
    )

    app.register_blueprint(
        ai_final_api
    )

    app.register_blueprint(
        ai_health_api
    )

    app.register_blueprint(
        ai_usage_api
    )

    app.register_blueprint(
        ai_security_api_v2
    )

    app.register_blueprint(
        ai_chat_api_v2
    )

    return app
