SEVERITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "info": 0
}


def triage_findings(findings):
    findings = list(
        findings or []
    )

    for finding in findings:
        severity = str(
            finding.get(
                "severity",
                "info"
            )
        ).lower()

        finding["_priority"] = (
            SEVERITY_ORDER.get(
                severity,
                0
            )
        )

    findings.sort(
        key=lambda item: item["_priority"],
        reverse=True
    )

    for finding in findings:
        finding.pop(
            "_priority",
            None
        )

    return findings


def summarize_findings(findings):
    ordered = triage_findings(
        findings
    )

    summary = {
        "total": len(ordered),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }

    for finding in ordered:
        severity = str(
            finding.get(
                "severity",
                "info"
            )
        ).lower()

        if severity not in summary:
            severity = "info"

        summary[severity] += 1

    return summary
