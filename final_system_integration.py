def integrate_final_system(app):
    from ai_routes_registration import register_ai_routes

    register_ai_routes(app)

    try:
        from security_bootstrap import bootstrap_security
        bootstrap_security(app)
    except ImportError:
        pass

    return app
