import os
from datetime import datetime


class AISecurityEngine:
    """
    Central AI security engine.

    This module is intentionally provider-agnostic.
    A real AI provider can be connected later using
    the AI_API_KEY environment variable.
    """

    def __init__(self):
        self.api_key = os.getenv(
            "AI_API_KEY",
            ""
        )

    def analyze(self, security_data):
        if not isinstance(security_data, dict):
            return {
                "success": False,
                "error": "Invalid security data."
            }

        risk_score = self._calculate_score(
            security_data
        )

        risk_level = self._risk_level(
            risk_score
        )

        recommendations = self._recommendations(
            risk_level
        )

        return {
            "success": True,
            "engine": "AI Security Brain",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendations": recommendations,
            "provider_connected": bool(
                self.api_key
            ),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _calculate_score(self, data):
        score = 0

        if data.get("suspicious_activity"):
            score += 35

        if data.get("unknown_device"):
            score += 25

        if data.get("weak_password"):
            score += 20

        if data.get("missing_2fa"):
            score += 15

        if data.get("privacy_risk"):
            score += 15

        return min(score, 100)

    def _risk_level(self, score):
        if score >= 80:
            return "critical"

        if score >= 60:
            return "high"

        if score >= 35:
            return "medium"

        return "low"

    def _recommendations(self, level):
        if level == "critical":
            return [
                "Review account activity immediately.",
                "Change exposed passwords.",
                "Enable two-factor authentication.",
                "Review unknown devices and sessions."
            ]

        if level == "high":
            return [
                "Review recent security activity.",
                "Enable two-factor authentication.",
                "Remove unknown sessions."
            ]

        if level == "medium":
            return [
                "Review security settings.",
                "Use unique passwords.",
                "Check recent account activity."
            ]

        return [
            "Continue monitoring your security."
        ]


ai_engine = AISecurityEngine()
