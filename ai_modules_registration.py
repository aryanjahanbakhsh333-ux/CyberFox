def register_ai_modules(app):

    from ai_security_api_v2 import (
        ai_security_api_v2
    )

    from ai_chat_api_v2 import (
        ai_chat_api_v2
    )

    app.register_blueprint(
        ai_security_api_v2
    )

    app.register_blueprint(
        ai_chat_api_v2
    )

    return app
