from datetime import datetime


class ThreatIntelligence:

    def __init__(self):
        self.sources = []

    def add_source(
        self,
        name,
        source_type
    ):
        self.sources.append({
            "name": name,
            "type": source_type,
            "added_at": datetime.utcnow().isoformat()
        })

    def status(self):
        return {
            "available": bool(self.sources),
            "source_count": len(self.sources),
            "sources": self.sources
        }

    def analyze_indicator(
        self,
        indicator,
        indicator_type
    ):
        if not indicator:
            return {
                "success": False,
                "error": "Indicator is required."
            }

        return {
            "success": True,
            "indicator": indicator,
            "type": indicator_type,
            "status": "unknown",
            "confidence": 0,
            "checked_at": datetime.utcnow().isoformat()
        }
