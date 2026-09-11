from database import db
from threat_models import Threat


SEVERITY_LEVELS = {
    "low",
    "medium",
    "high",
    "critical"
}


def create_threat(
    user_id,
    threat_type,
    title,
    description,
    severity="low"
):
    if severity not in SEVERITY_LEVELS:
        severity = "low"

    threat = Threat(
        user_id=user_id,
        threat_type=threat_type,
        title=title,
        description=description,
        severity=severity,
        status="detected"
    )

    db.session.add(threat)
    db.session.commit()

    return threat


def get_user_threats(user_id):
    return Threat.query.filter_by(
        user_id=user_id
    ).order_by(
        Threat.created_at.desc()
    ).all()
