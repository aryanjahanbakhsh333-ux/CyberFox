from plan_service import get_plan_features
from user_service import get_user_profile


def build_dashboard(user):
    return {
        "user": get_user_profile(user),
        "plan": {
            "name": user.plan,
            "features": get_plan_features(
                user.plan
            )
        },
        "security": {
            "status": "not_assessed",
            "score": None
        }
    }
