import os


def get_ai_health():
    api_key = os.getenv(
        "AI_API_KEY",
        ""
    ).strip()

    base_url = os.getenv(
        "AI_BASE_URL",
        ""
    ).strip()

    model = os.getenv(
        "AI_MODEL",
        ""
    ).strip()

    return {
        "service": "ai",
        "configured": bool(
            api_key and base_url and model
        ),
        "provider": (
            os.getenv(
                "AI_PROVIDER",
                "generic"
            )
        ),
        "model": model or None
    }
