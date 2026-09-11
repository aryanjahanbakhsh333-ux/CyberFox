from smtp_email_provider import (
    SMTPEmailProvider
)


_provider = SMTPEmailProvider()


def send_verification_email(
    email,
    code
):
    subject = (
        "Verify your security platform account"
    )

    text = (
        "Your verification code is: "
        f"{code}\n\n"
        "This code expires shortly."
    )

    return _provider.send(
        email,
        subject,
        text
    )


def send_password_reset_email(
    email,
    reset_url
):
    subject = "Reset your security platform password"

    text = (
        "A password reset was requested "
        "for your account.\n\n"
        f"Reset your password here:\n{reset_url}\n\n"
        "If you did not request this, ignore this email."
    )

    return _provider.send(
        email,
        subject,
        text
    )


def send_security_alert(
    email,
    title,
    message
):
    return _provider.send(
        email,
        title,
        message
    )
