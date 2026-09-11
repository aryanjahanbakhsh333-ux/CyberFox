import re


SUSPICIOUS_PATTERNS = [
    r"verify\s+your\s+account",
    r"account\s+suspended",
    r"urgent\s+payment",
    r"send\s+money",
    r"claim\s+your\s+prize",
    r"gift\s+card",
    r"confirm\s+your\s+password",
    r"login\s+immediately",
    r"security\s+alert"
]


def detect_phishing(text):

    if not isinstance(
        text,
        str
    ):
        return {
            "detected": False,
            "risk": "unknown",
            "matches": []
        }

    matches = []

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            matches.append(
                pattern
            )

    if len(matches) >= 3:
        risk = "high"
    elif len(matches) == 2:
        risk = "medium"
    elif len(matches) == 1:
        risk = "low"
    else:
        risk = "none"

    return {
        "detected": bool(matches),
        "risk": risk,
        "matches": matches
    }
