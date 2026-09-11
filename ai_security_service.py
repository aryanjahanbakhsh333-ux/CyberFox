import json

from ai_provider import (
    AIProvider,
    AIProviderError
)


SYSTEM_PROMPT = """
You are a defensive cybersecurity analysis engine.

Only analyze systems, accounts, devices,
files, URLs, or servers that the user owns
or is explicitly authorized to assess.

Do not provide instructions for credential theft,
unauthorized access, malware deployment,
exploitation of third-party systems,
or bypassing authentication.

Return structured defensive analysis.
"""


def analyze_security_context(context):

    provider = AIProvider()

    if not provider.is_configured():
        return {
            "success": False,
            "status": "not_configured",
            "error": "AI provider is not configured."
        }

    prompt = json.dumps(
        context,
        ensure_ascii=False
    )

    try:
        result = provider.analyze(
            SYSTEM_PROMPT,
            prompt
        )

        return {
            "success": True,
            "status": "analyzed",
            "result": result
        }

    except AIProviderError as exc:
        return {
            "success": False,
            "status": "error",
            "error": str(exc)
        }
