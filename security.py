from datetime import datetime


ALLOWED_TARGET_TYPES = {
    "device",
    "account",
    "website",
    "server"
}


def validate_target(target_type):
    if target_type not in ALLOWED_TARGET_TYPES:
        return {
            "valid": False,
            "error": "Unsupported target type."
        }

    return {
        "valid": True,
        "target": target_type
    }


def create_security_event(
    event_type,
    description,
    severity="info"
):
    return {
        "event_type": event_type,
        "description": description,
        "severity": severity,
        "created_at": datetime.utcnow().isoformat()
    }


def security_assessment(target_type):
    validation = validate_target(target_type)

    if not validation["valid"]:
        return validation

    return {
        "success": True,
        "target": target_type,
        "status": "not_assessed",
        "message": (
            "A security assessment has not "
            "been performed yet."
        )
    }
