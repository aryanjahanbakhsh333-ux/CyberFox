from enum import Enum


class DefenseMode(str, Enum):
    OBSERVE = "observe"
    RECOMMEND = "recommend"
    CONFIRM = "confirm"
    AUTO_DEFEND = "auto_defend"


SAFE_ACTIONS = {
    "revoke_own_sessions",
    "disable_own_api_token",
    "block_known_malicious_url",
    "increase_security_monitoring",
    "require_2fa"
}


def is_action_allowed(
    action,
    mode,
    authorized=True
):
    if not authorized:
        return False

    if action not in SAFE_ACTIONS:
        return False

    if mode == DefenseMode.OBSERVE:
        return False

    if mode == DefenseMode.RECOMMEND:
        return False

    if mode == DefenseMode.CONFIRM:
        return True

    if mode == DefenseMode.AUTO_DEFEND:
        return True

    return False


def build_defense_decision(
    action,
    mode,
    authorized=True
):
    allowed = is_action_allowed(
        action,
        mode,
        authorized
    )

    return {
        "action": action,
        "mode": mode,
        "authorized": authorized,
        "allowed": allowed,
        "requires_confirmation": (
            mode == DefenseMode.CONFIRM
            and allowed
        ),
        "reason": (
            "Action is permitted by the "
            "defensive policy."
            if allowed
            else
            "Action is blocked by the "
            "defensive policy."
        )
    }
