from datetime import datetime


class IdentityProtection:

    def analyze(self, data):
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "Invalid identity data."
            }

        risks = []

        if data.get("password_reuse"):
            risks.append({
                "type": "password_reuse",
                "severity": "high",
                "message": (
                    "Password reuse may increase account risk."
                )
            })

        if data.get("personal_data_exposed"):
            risks.append({
                "type": "personal_data_exposure",
                "severity": "high",
                "message": (
                    "Personal information may be exposed."
                )
            })

        if data.get("suspicious_login"):
            risks.append({
                "type": "suspicious_login",
                "severity": "high",
                "message": (
                    "A suspicious login requires review."
                )
            })

        return {
            "success": True,
            "protected": len(risks) == 0,
            "risk_count": len(risks),
            "risks": risks,
            "timestamp": datetime.utcnow().isoformat()
        }


identity_protection = IdentityProtection()
