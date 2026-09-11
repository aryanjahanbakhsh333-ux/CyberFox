from datetime import datetime


def build_monitoring_status():
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "api": "online",
            "database": "online",
            "authentication": "online",
            "security_engine": "online",
            "billing": "online",
            "monitoring": "online"
        }
    }


def build_metric(
    name,
    value,
    unit=None
):
    return {
        "name": name,
        "value": value,
        "unit": unit,
        "timestamp": datetime.utcnow().isoformat()
    }
