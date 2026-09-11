from datetime import datetime

from ai_threat_triage import (
    summarize_findings,
    triage_findings
)

from ai_recommendation_service import (
    generate_recommendations
)


def build_ai_report(
    target,
    findings,
    ai_analysis=None
):
    ordered = triage_findings(
        findings
    )

    return {
        "generated_at":
            datetime.utcnow().isoformat(),

        "target": target,

        "summary":
            summarize_findings(
                ordered
            ),

        "findings": ordered,

        "recommendations":
            generate_recommendations(
                ordered
            ),

        "ai_analysis":
            ai_analysis
    }
