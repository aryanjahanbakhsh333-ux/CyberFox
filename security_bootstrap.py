def bootstrap_security(app):
    from auth_security_model import AuthSecurity
    from audit_model import AuditLog
    from webhook_event_model import WebhookEvent
    from device_fleet_model import ManagedDevice

    # Importing models before create_all()
    # guarantees their metadata is registered.
    with app.app_context():
        from database import db
        db.create_all()

    return app
