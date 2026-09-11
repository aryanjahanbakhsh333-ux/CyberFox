from urllib.parse import (
    urlparse
)


def analyze_url(url):

    if not isinstance(
        url,
        str
    ):
        return {
            "safe": False,
            "risk": "high",
            "reason": "Invalid URL format."
        }

    url = url.strip()

    parsed = urlparse(url)

    if parsed.scheme not in {
        "http",
        "https"
    }:
        return {
            "safe": False,
            "risk": "high",
            "reason": "Unsupported URL scheme."
        }

    if not parsed.netloc:
        return {
            "safe": False,
            "risk": "high",
            "reason": "URL has no valid host."
        }

    hostname = parsed.hostname

    if not hostname:
        return {
            "safe": False,
            "risk": "high",
            "reason": "Hostname could not be identified."
        }

    risk = "low"
    reasons = []

    if parsed.scheme != "https":
        risk = "medium"
        reasons.append(
            "Connection does not use HTTPS."
        )

    if "@" in url:
        risk = "high"
        reasons.append(
            "URL contains an embedded user-info section."
        )

    return {
        "safe": risk == "low",
        "risk": risk,
        "hostname": hostname,
        "reasons": reasons
    }
