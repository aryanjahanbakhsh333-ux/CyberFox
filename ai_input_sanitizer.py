MAX_TEXT_LENGTH = 12000
MAX_ITEMS = 100


def sanitize_text(value):
    if not isinstance(value, str):
        return ""

    value = value.strip()

    return value[:MAX_TEXT_LENGTH]


def sanitize_findings(findings):
    if not isinstance(findings, list):
        return []

    clean = []

    for item in findings[:MAX_ITEMS]:
        if not isinstance(item, dict):
            continue

        clean.append({
            "type": sanitize_text(
                item.get("type", "")
            )[:100],
            "severity": sanitize_text(
                item.get(
                    "severity",
                    "info"
                )
            )[:20],
            "description": sanitize_text(
                item.get(
                    "description",
                    ""
                )
            )
        })

    return clean


def sanitize_ai_request(data):
    if not isinstance(data, dict):
        return {}

    return {
        "target": sanitize_text(
            data.get(
                "target",
                "unknown"
            )
        )[:100],

        "message": sanitize_text(
            data.get(
                "message",
                ""
            )
        ),

        "findings":
            sanitize_findings(
                data.get(
                    "findings",
                    []
                )
            ),

        "context":
            data.get(
                "context",
                {}
            )
            if isinstance(
                data.get(
                    "context",
                    {}
                ),
                dict
            )
            else {}
    }
