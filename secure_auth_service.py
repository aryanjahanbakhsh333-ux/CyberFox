from auth_service import authenticate_user

from login_security import (
    check_login_allowed,
    register_failed_login,
    register_successful_login
)

from secure_session import secure_sessions


def secure_login(
    email,
    password
):
    identifier = email.strip().lower()

    if not check_login_allowed(
        identifier
    ):
        return {
            "success": False,
            "error": (
                "Too many failed login attempts. "
                "Please try again later."
            )
        }

    user = authenticate_user(
        identifier,
        password
    )

    if not user:
        register_failed_login(
            identifier
        )

        return {
            "success": False,
            "error": "Invalid email or password."
        }

    register_successful_login(
        identifier
    )

    token = secure_sessions.create(
        user.id
    )

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "plan": user.plan,
            "role": user.role
        }
    }
