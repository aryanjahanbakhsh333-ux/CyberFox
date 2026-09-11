from datetime import datetime


class ThreatDetector:

    def detect(self, data):
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "Invalid threat data."
            }

        findings = []

        if data.get("suspicious_activity"):
            findings.append({
                "type": "suspicious_activity",
                "severity": "high",
                "message": (
                    "Suspicious activity was detected."
                )
            })

        if data.get("unknown_device"):
            findings.append({
                "type": "unknown_device",
                "severity": "medium",
                "message": (
                    "An unknown device may be connected."
                )
            })

        if data.get("weak_password"):
            findings.append({
                "type": "weak_password",
                "severity": "medium",
                "message": (
                    "The account may be using a weak password."
                )
            })

        if data.get("missing_2fa"):
            findings.append({
                "type": "missing_2fa",
                "severity": "medium",
                "message": (
                    "Two-factor authentication is not enabled."
                )
            })

        return {
            "success": True,
            "detected": len(findings) > 0,
            "count": len(findings),
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }


threat_detector = ThreatDetector()
