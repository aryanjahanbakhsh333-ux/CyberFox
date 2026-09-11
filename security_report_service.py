from datetime import datetime


def build_security_report(
    user,
    score,
    threats,
    prediction,
    recommendations
):
    return {
        "generated_at":
            datetime.utcnow().isoformat(),

        "account": {
            "id": user.id,
            "plan": user.plan
        },

        "security_score": score,

        "threats": threats,

        "threat_prediction": prediction,

        "recommendations":
            recommendations
    }
