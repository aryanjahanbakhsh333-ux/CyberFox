RECOMMENDATIONS = {
    "weak_password": (
        "Replace the password with a unique strong "
        "password."
    ),
    "missing_2fa": (
        "Enable two-factor authentication."
    ),
    "unknown_device": (
        "Review the device and revoke access if "
        "you do not recognize it."
    ),
    "suspicious_login": (
        "Review recent login activity and revoke "
        "unrecognized sessions."
    ),
    "phishing": (
        "Do not follow the suspicious link or submit "
        "credentials."
    ),
    "privacy_exposure": (
        "Reduce publicly exposed personal information."
    ),
    "outdated_software": (
        "Install security updates from the official "
        "software vendor."
    )
}


def generate_recommendations(
    findings
):
    results = []
    seen = set()

    for finding in findings or []:
        finding_type = str(
            finding.get(
                "type",
                ""
            )
        ).lower()

        recommendation = (
            RECOMMENDATIONS.get(
                finding_type
            )
        )

        if (
            recommendation
            and recommendation not in seen
        ):
            results.append({
                "type": finding_type,
                "recommendation":
                    recommendation,
                "severity":
                    finding.get(
                        "severity",
                        "info"
                    )
            })

            seen.add(
                recommendation
            )

    return results
