from datetime import datetime


def get_system_health():
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "online",
            "database": "online",
            "authentication": "online",
            "security_engine": "online"
        }
    }
