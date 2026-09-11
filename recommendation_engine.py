def generate_recommendations(
    risk_level
):
    recommendations = []

    if risk_level == "critical":
        recommendations.extend([
            "Review active sessions immediately.",
            "Change the account password.",
            "Enable two-factor authentication.",
            "Review recent security activity."
        ])

    elif risk_level == "high":
        recommendations.extend([
            "Review account activity.",
            "Use a strong unique password.",
            "Enable two-factor authentication."
        ])

    elif risk_level == "medium":
        recommendations.extend([
            "Review your security settings.",
            "Use a unique password."
        ])

    else:
        recommendations.append(
            "Continue monitoring your security."
        )

    return recommendations
