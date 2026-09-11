from security import security_assessment
from plan_service import is_pro_user


def analyze_target(user, target_type):
    assessment = security_assessment(
        target_type
    )

    if not assessment.get("success"):
        return assessment

    return {
        "success": True,
        "target": target_type,
        "plan": user.plan,
        "pro_features": is_pro_user(user),
        "status": "assessment_ready",
        "message": (
            "The target is ready for a "
            "security assessment."
        )
    }
