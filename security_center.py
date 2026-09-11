from ai_security import ai_brain
from recommendation_engine import (
    generate_recommendations
)
from risk_engine import calculate_risk


class SecurityCenter:

    def analyze(self, data):
        severity = data.get(
            "severity",
            "low"
        )

        suspicious_activity = data.get(
            "suspicious_activity",
            False
        )

        risk = calculate_risk(
            severity,
            suspicious_activity
        )

        recommendations = (
            generate_recommendations(
                risk["level"]
            )
        )

        ai_result = ai_brain.analyze(
            data
        )

        return {
            "risk": risk,
            "recommendations": recommendations,
            "ai": ai_result
        }


security_center = SecurityCenter()
