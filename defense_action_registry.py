SAFE_DEFENSIVE_ACTIONS = {
    "revoke_own_sessions": {
        "risk": "low",
        "reversible": True
    },
    "require_2fa": {
        "risk": "low",
        "reversible": True
    },
    "increase_monitoring": {
        "risk": "low",
        "reversible": True
    },
    "block_malicious_url": {
        "risk": "medium",
        "reversible": True
    }
}


def get_action(action):
    return SAFE_DEFENSIVE_ACTIONS.get(
        action
    )


def is_registered(action):
    return action in SAFE_DEFENSIVE_ACTIONS
