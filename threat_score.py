SEVERITY_WEIGHTS = {
    "none": 0,
    "low": 20,
    "medium": 50,
    "high": 80,
    "critical": 100
}


def calculate_threat_score(
    findings
):

    if not findings:
        return {
            "score": 0,
            "level": "none"
        }

    scores = []

    for finding in findings:

        severity = str(
            finding.get(
                "severity",
                "none"
            )
        ).lower()

        scores.append(
            SEVERITY_WEIGHTS.get(
                severity,
                0
            )
        )

    score = max(
        scores
    ) if scores else 0

    if score >= 90:
        level = "critical"
    elif score >= 70:
        level = "high"
    elif score >= 40:
        level = "medium"
    elif score > 0:
        level = "low"
    else:
        level = "none"

    return {
        "score": score,
        "level": level
    }
