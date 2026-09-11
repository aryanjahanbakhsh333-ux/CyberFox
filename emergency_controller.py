from database import db
from session_service import delete_session


def activate_emergency(
    user_id,
    current_token=None
):
    actions = []

    if current_token:
        delete_session(
            current_token
        )
        actions.append(
            "current_session_revoked"
        )

    actions.extend([
        "security_monitoring_requested",
        "account_review_requested",
        "security_notification_requested"
    ])

    return {
        "success": True,
        "user_id": user_id,
        "mode": "emergency",
        "actions": actions,
        "automatic_external_changes": False
    }


def revoke_all_known_sessions(
    user_id
):
    return {
        "success": True,
        "user_id": user_id,
        "action": "session_revocation_requested"
    }
