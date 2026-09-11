FEATURES = {
    "advanced_ai": {
        "free": False,
        "pro": True
    },
    "device_security": {
        "free": False,
        "pro": True
    },
    "server_guardian": {
        "free": False,
        "pro": True
    },
    "advanced_defense": {
        "free": False,
        "pro": True
    },
    "threat_prediction": {
        "free": True,
        "pro": True
    },
    "phishing_scanner": {
        "free": True,
        "pro": True
    },
    "privacy_scanner": {
        "free": True,
        "pro": True
    },
    "lock_recovery": {
        "free": True,
        "pro": True
    },
    "password_recovery": {
        "free": True,
        "pro": True
    }
}


def feature_available(
    feature,
    plan
):
    definition = FEATURES.get(feature)

    if not definition:
        return False

    return bool(
        definition.get(
            plan,
            False
        )
    )


def list_features(plan):
    return {
        name: feature_available(
            name,
            plan
        )
        for name in FEATURES
    }
