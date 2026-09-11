from defense_action_registry import (
    get_action,
    is_registered
)


class DefenseExecutionError(Exception):
    pass


def execute_defensive_action(
    action,
    authorized=False,
    confirmed=False
):
    if not authorized:
        raise DefenseExecutionError(
            "Authorized scope is required."
        )

    if not is_registered(action):
        raise DefenseExecutionError(
            "Action is not allowed."
        )

    if not confirmed:
        return {
            "executed": False,
            "action": action,
            "reason": "Confirmation required."
        }

    metadata = get_action(action)

    return {
        "executed": True,
        "action": action,
        "risk": metadata["risk"],
        "reversible": metadata["reversible"]
    }
