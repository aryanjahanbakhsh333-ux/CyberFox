from ai_chat_service import (
    SecurityChatService
)

from ai_security_orchestrator import (
    AISecurityOrchestrator
)


TOOLS = {
    "security_analysis": (
        AISecurityOrchestrator
    ),
    "security_chat": (
        SecurityChatService
    )
}


def available_tools():
    return list(
        TOOLS.keys()
    )


def create_tool(name):
    tool = TOOLS.get(name)

    if not tool:
        raise ValueError(
            "Unknown AI tool."
        )

    return tool()
