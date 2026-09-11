from datetime import datetime

from ai_engine import AISecurityEngine
from ai_threat_triage import triage_findings, summarize_findings
from ai_recommendation_service import generate_recommendations
from threat_detector import detect_threats
from phishing_detector import detect_phishing
from scam_hunter import scan_scam
from privacy_scanner import scan_privacy
from threat_prediction_service import ThreatPredictionService


class AIFinalPipeline:
    def __init__(self):
        self.ai = AISecurityEngine()
        self.predictor = ThreatPredictionService()

    def analyze(
        self,
        target,
        data=None,
        message=None,
        privacy_data=None
    ):
        data = data or {}

        findings = []

        findings.extend(
            detect_threats(data)
        )

        if message:
            phishing = detect_phishing(message)

            if phishing.get("suspicious"):
                findings.append({
                    "type": "phishing",
                    "severity": "high",
                    "description":
                        phishing.get(
                            "reason",
                            "Suspicious message detected."
                        )
                })

            scam = scan_scam(message)

            if scam.get("suspicious"):
                findings.append({
                    "type": "scam",
                    "severity": "high",
                    "description":
                        scam.get(
                            "reason",
                            "Potential scam detected."
                        )
                })

        if privacy_data:
            privacy = scan_privacy(
                privacy_data
            )

            if privacy.get("risk"):
                findings.append({
                    "type": "privacy_exposure",
                    "severity": "medium",
                    "description":
                        "Potential privacy exposure detected."
                })

        findings = triage_findings(
            findings
        )

        ai_result = self.ai.analyze(
            data
        )

        prediction = self.predictor.predict(
            findings
        )

        return {
            "success": True,
            "generated_at":
                datetime.utcnow().isoformat(),
            "target": target,
            "summary":
                summarize_findings(findings),
            "findings": findings,
            "recommendations":
                generate_recommendations(
                    findings
                ),
            "ai": ai_result,
            "prediction": prediction
        }
