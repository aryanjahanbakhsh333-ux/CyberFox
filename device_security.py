from datetime import datetime


class DeviceSecurity:

    ALLOWED_DEVICE_TYPES = {
        "phone",
        "tablet",
        "computer",
        "browser"
    }

    def inspect(self, device):
        if not isinstance(device, dict):
            return {
                "success": False,
                "error": "Invalid device data."
            }

        device_type = device.get(
            "type",
            "unknown"
        )

        if device_type not in self.ALLOWED_DEVICE_TYPES:
            return {
                "success": False,
                "error": "Unsupported device type."
            }

        findings = []

        if device.get("outdated"):
            findings.append({
                "issue": "outdated_software",
                "severity": "medium"
            })

        if device.get("unknown_app"):
            findings.append({
                "issue": "unknown_application",
                "severity": "high"
            })

        if device.get("rooted_or_modified"):
            findings.append({
                "issue": "device_integrity",
                "severity": "high"
            })

        return {
            "success": True,
            "device_type": device_type,
            "secure": len(findings) == 0,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }


device_security = DeviceSecurity()
