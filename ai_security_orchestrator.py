from ai_provider_real import (
    HTTPAIProvider,
    AIProviderError
)


SYSTEM_PROMPT = """
You are a defensive cybersecurity AI.

Your job is to help users protect systems,
accounts, devices and data they own or are
authorized to manage.

You may:
- analyze security findings
- explain risks
- detect suspicious behavior
- prioritize vulnerabilities
- recommend defensive actions
- explain phishing and scams
- create security checklists
- summarize security events
- suggest safe remediation

You must not:
- steal credentials
- bypass authentication
- access unauthorized accounts
- provide malware
- provide destructive attack instructions
- attack third-party systems
- perform unauthorized exploitation

Always prefer defensive, reversible and
auditable recommendations.
"""


class AISecurityOrchestrator:

    def __init__(self):
        self.provider = HTTPAIProvider()

    def analyze(
        self,
        target,
        findings,
        context=None
    ):
        prompt = {
            "target": target,
            "findings": findings,
            "context": context or {}
        }

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": str(prompt)
            }
        ]

        if not self.provider.available():
            return {
                "success": True,
                "provider": "local",
                "analysis": self._local_analysis(
                    findings
                )
            }

        try:
            answer = self.provider.chat(
                messages
            )

            return {
                "success": True,
                "provider": "ai",
                "analysis": answer
            }

        except AIProviderError:
            return {
                "success": True,
                "provider": "local",
                "analysis": self._local_analysis(
                    findings
                )
            }

    def _local_analysis(self, findings):
        findings = findings or []

        if not findings:
            return (
                "No security findings were provided. "
                "Run a security scan first."
            )

        critical = 0
        high = 0
        medium = 0

        for finding in findings:
            severity = str(
                finding.get(
                    "severity",
                    "low"
                )
            ).lower()

            if severity == "critical":
                critical += 1

            elif severity == "high":
                high += 1

            elif severity == "medium":
                medium += 1

        if critical:
            priority = "critical"
        elif high:
            priority = "high"
        elif medium:
            priority = "medium"
        else:
            priority = "low"

        return {
            "priority": priority,
            "critical_findings": critical,
            "high_findings": high,
            "medium_findings": medium,
            "recommendation": (
                "Address the highest-severity findings "
                "first and enable stronger account "
                "protection."
            )
        }
