from datetime import datetime


class DefenseEngine:

    def recommend_actions(self, findings):
        if not isinstance(findings, list):
            return {
                "success": False,
                "error": "Invalid findings."
            }

        actions = []

        for finding in findings:
            issue = finding.get(
                "issue",
                ""
            )

            if issue == "outdated_software":
                actions.append({
                    "action": "recommend_update",
                    "automatic": False
                })

            elif issue == "weak_configuration":
                actions.append({
                    "action": "recommend_configuration_review",
                    "automatic": False
                })

            elif issue == "exposed_service":
                actions.append({
                    "action": "recommend_service_review",
                    "automatic": False
                })

            elif issue == "unknown_application":
                actions.append({
                    "action": "recommend_application_review",
                    "automatic": False
                })

        return {
            "success": True,
            "actions": actions,
            "timestamp": datetime.utcnow().isoformat()
        }


defense_engine = DefenseEngine()
