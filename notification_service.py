from datetime import datetime


def create_notification(
    title,
    message,
    notification_type="info"
):
    return {
        "title": title,
        "message": message,
        "type": notification_type,
        "created_at": datetime.utcnow().isoformat(),
        "read": False
    }
