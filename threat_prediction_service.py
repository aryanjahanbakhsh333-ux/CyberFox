from datetime import datetime


WEIGHTS = {
    "critical": 40,
    "high": 25,
    "medium": 12,
    "low": 4,
    "info": 1
}


def predict_threat(findings):
    score = 0

    for finding in findings or []:
        severity = str(
            finding.get(
                "severity",
                "info"
            )
        ).lower()

        score += WEIGHTS.get(
            severity,
            1
        )

    score = min(
        100,
        score
    )

    if score >= 75:
        level = "critical"
    elif score >= 50:
        level = "high"
    elif score >= 25:
        level = "medium"
    else:
        level = "low"

    return {
        "score": score,
        "level": level,
        "predicted_at":
            datetime.utcnow().isoformat()
    }
