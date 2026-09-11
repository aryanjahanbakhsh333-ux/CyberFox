def calculate_security_score(
    has_strong_password=False,
    has_two_factor=False,
    recent_security_check=False,
    suspicious_activity=False
):
    score = 0

    if has_strong_password:
        score += 30

    if has_two_factor:
        score += 30

    if recent_security_check:
        score += 20

    if not suspicious_activity:
        score += 20

    return min(score, 100)


def score_level(score):
    if score >= 80:
        return "strong"

    if score >= 60:
        return "good"

    if score >= 40:
        return "needs_attention"

    return "weak"
