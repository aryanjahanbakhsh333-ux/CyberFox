from models import User

from owner_service import (
    is_owner
)


def verify_owner(user):
    if not user:
        return False

    return is_owner(user)


def get_owner_overview(user):
    if not verify_owner(user):
        return {
            "authorized": False
        }

    return {
        "authorized": True,
        "owner_id": user.id,
        "email": user.email,
        "role": user.role,
        "plan": user.plan
    }


def find_user(user_id):
    return User.query.get(user_id)
