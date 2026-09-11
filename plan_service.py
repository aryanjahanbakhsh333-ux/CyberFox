FREE_PLAN = "free"
PRO_PLAN = "pro"


def normalize_plan(plan):
    if plan == PRO_PLAN:
        return PRO_PLAN

    return FREE_PLAN


def is_pro_user(user):
    if not user:
        return False

    return normalize_plan(user.plan) == PRO_PLAN


def get_plan_features(plan):
    plan = normalize_plan(plan)

    if plan == PRO_PLAN:
        return {
            "security_analysis": True,
            "account_security": True,
            "device_security": True,
            "server_security": True,
            "advanced_ai": True,
            "autonomous_defense": True,
            "owner_tools": False
        }

    return {
        "security_analysis": True,
        "account_security": True,
        "device_security": False,
        "server_security": False,
        "advanced_ai": False,
        "autonomous_defense": False,
        "owner_tools": False
    }
