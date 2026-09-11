import os


class EmailService:

    def __init__(self):
        self.sender = os.getenv(
            "EMAIL_SENDER",
            ""
        )

    def send_verification_code(
        self,
        email,
        code
    ):
        if not self.sender:
            return {
                "success": False,
                "error": (
                    "Email service is not configured."
                )
            }

        # Real email provider integration
        # will be connected here.
        return {
            "success": True,
            "message": (
                "Verification email queued."
            )
        }

    def send_password_reset_code(
        self,
        email,
        code
    ):
        if not self.sender:
            return {
                "success": False,
                "error": (
                    "Email service is not configured."
                )
            }

        return {
            "success": True,
            "message": (
                "Password reset email queued."
            )
        }


email_service = EmailService()
