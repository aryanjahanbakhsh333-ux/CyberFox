from models import User


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_profile(user):
    if not user:
        return None

    return {
        "id": user.id,
        "email": user.email,
        "plan": user.plan,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": (
            user.created_at.isoformat()
            if user.created_at
            else None
        ),
        "last_login": (
            user.last_login.isoformat()
            if user.last_login
            else None
        )
    }
