import json

from database import db
from audit_model import AuditLog


def record_audit(
    user_id,
    action,
    resource=None,
    result="success",
    ip_address=None,
    user_agent=None,
    details=None
):
    if details is not None:
        details = json.dumps(
            details,
            ensure_ascii=False
        )

    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        result=result,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )

    db.session.add(log)
    db.session.commit()

    return log


def get_user_audit_logs(
    user_id,
    limit=100
):
    return (
        AuditLog.query
        .filter_by(user_id=user_id)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )


def serialize_audit(log):
    return {
        "id": log.id,
        "action": log.action,
        "resource": log.resource,
        "result": log.result,
        "details": log.details,
        "created_at": (
            log.created_at.isoformat()
            if log.created_at
            else None
        )
    }
