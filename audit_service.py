from datetime import datetime

from database import db


def create_audit_record(
    action,
    user_id=None,
    result="success"
):
    return {
        "action": action,
        "user_id": user_id,
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    }
