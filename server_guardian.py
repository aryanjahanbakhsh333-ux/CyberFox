from plan_service import is_pro_user


class ServerGuardian:

    def check_access(self, user):
        if not user:
            return {
                "allowed": False,
                "reason": "Authentication required."
            }

        if not is_pro_user(user):
            return {
                "allowed": False,
                "reason": "Pro plan required."
            }

        return {
            "allowed": True,
            "reason": (
                "Authorized server security "
                "features are available."
            )
        }


server_guardian = ServerGuardian()
