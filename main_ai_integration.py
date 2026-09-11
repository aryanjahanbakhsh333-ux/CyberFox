def integrate_final_ai(app):
    from ai_routes_registration import (
        register_ai_routes
    )

    register_ai_routes(app)

    return app
