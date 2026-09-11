from datetime import datetime


class PrivacyScanner:

    def scan(self, data):
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "Invalid privacy data."
            }

        risks = []

        if data.get("public_email"):
            risks.append({
                "type": "public_email",
                "severity": "low"
            })

        if data.get("public_phone"):
            risks.append({
                "type": "public_phone",
                "severity": "medium"
            })

        if data.get("public_location"):
            risks.append({
                "type": "public_location",
                "severity": "high"
            })

        if data.get("public_personal_information"):
            risks.append({
                "type": "personal_information",
                "severity": "high"
            })

        return {
            "success": True,
            "privacy_score": self._score(
                len(risks)
            ),
            "risks": risks,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _score(self, risk_count):
        score = 100 - (
            risk_count * 20
        )

        return max(score, 0)


privacy_scanner = PrivacyScanner()
