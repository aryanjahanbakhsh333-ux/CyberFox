from datetime import datetime


class ServerSecurity:

    def inspect_authorized_server(
        self,
        user,
        server
    ):
        if not user:
            return {
                "success": False,
                "error": "Authentication required."
            }

        if user.plan != "pro":
            return {
                "success": False,
                "error": "Pro plan required."
            }

        if not isinstance(server, dict):
            return {
                "success": False,
                "error": "Invalid server data."
            }

        if not server.get("authorized"):
            return {
                "success": False,
                "error": (
                    "Server authorization is required."
                )
            }

        findings = []

        if server.get("outdated_software"):
            findings.append({
                "issue": "outdated_software",
                "severity": "medium"
            })

        if server.get("weak_configuration"):
            findings.append({
                "issue": "weak_configuration",
                "severity": "high"
            })

        if server.get("exposed_service"):
            findings.append({
                "issue": "exposed_service",
                "severity": "high"
            })

        return {
            "success": True,
            "authorized": True,
            "findings": findings,
            "secure": len(findings) == 0,
            "timestamp": datetime.utcnow().isoformat()
        }


server_security = ServerSecurity()
