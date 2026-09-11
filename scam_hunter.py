from datetime import datetime


class ScamHunter:

    SUSPICIOUS_TERMS = {
        "urgent payment",
        "send money",
        "verify immediately",
        "claim your prize",
        "gift card",
        "crypto payment",
        "account suspended"
    }

    def analyze_text(self, text):
        if not isinstance(text, str):
            return {
                "success": False,
                "error": "Text must be a string."
            }

        normalized = text.lower()

        matches = [
            term
            for term in self.SUSPICIOUS_TERMS
            if term in normalized
        ]

        if len(matches) >= 3:
            level = "high"

        elif len(matches) >= 1:
            level = "medium"

        else:
            level = "low"

        return {
            "success": True,
            "risk_level": level,
            "suspicious": bool(matches),
            "matched_patterns": matches,
            "recommendation": self._recommendation(
                level
            ),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _recommendation(self, level):
        if level == "high":
            return (
                "Do not send money or sensitive information. "
                "Verify the sender independently."
            )

        if level == "medium":
            return (
                "Be cautious and verify the message "
                "before taking action."
            )

        return (
            "No obvious scam pattern was detected."
        )


scam_hunter = ScamHunter()
