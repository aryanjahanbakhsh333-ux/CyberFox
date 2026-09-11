import os
import smtplib
from email.message import EmailMessage

from email_provider import EmailProvider


class SMTPEmailProvider(
    EmailProvider
):
    def __init__(self):
        self.host = os.getenv(
            "SMTP_HOST",
            ""
        )

        self.port = int(
            os.getenv(
                "SMTP_PORT",
                "587"
            )
        )

        self.username = os.getenv(
            "SMTP_USERNAME",
            ""
        )

        self.password = os.getenv(
            "SMTP_PASSWORD",
            ""
        )

        self.sender = os.getenv(
            "EMAIL_SENDER",
            self.username
        )

    def send(
        self,
        recipient,
        subject,
        text,
        html=None
    ):
        if not all([
            self.host,
            self.username,
            self.password,
            self.sender
        ]):
            raise RuntimeError(
                "SMTP configuration is incomplete."
            )

        message = EmailMessage()

        message["From"] = self.sender
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(text)

        if html:
            message.add_alternative(
                html,
                subtype="html"
            )

        with smtplib.SMTP(
            self.host,
            self.port
        ) as server:
            server.starttls()

            server.login(
                self.username,
                self.password
            )

            server.send_message(
                message
            )

        return True
