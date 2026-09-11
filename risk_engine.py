SEVERITY_WEIGHTS = {
    "low": 20,
    "medium": 45,
    "high": 70,
    "critical": 95
}


def calculate_risk(
    severity="low",
    suspicious_activity=False
):
    score = SEVERITY_WEIGHTS.get(
        severity,
        20
    )

    if suspicious_activity:
        score += 10

    score = min(score, 100)

    if score >= 80:
        level = "critical"

    elif score >= 60:
        level = "high"

    elif score >= 35:
        level = "medium"

    else:
        level = "low"

    return {
        "score": score,
        "level": level
    }
