from ai_engine import ai_engine
from threat_detector import threat_detector
from identity_protection import identity_protection
from privacy_scanner import privacy_scanner
from scam_hunter import scam_hunter


class AdvancedSecurityCenter:

    def analyze(self, data):
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "Invalid security data."
            }

        threat_result = threat_detector.detect(
            data
        )

        identity_result = identity_protection.analyze(
            data
        )

        privacy_result = privacy_scanner.scan(
            data
        )

        ai_result = ai_engine.analyze(
            data
        )

        scam_result = None

        text = data.get("text")

        if isinstance(text, str) and text.strip():
            scam_result = scam_hunter.analyze_text(
                text
            )

        return {
            "success": True,
            "threats": threat_result,
            "identity": identity_result,
            "privacy": privacy_result,
            "ai": ai_result,
            "scam": scam_result
        }


advanced_security_center = AdvancedSecurityCenter()
