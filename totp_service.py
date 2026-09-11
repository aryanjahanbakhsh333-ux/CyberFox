import base64
import io
import secrets

import pyotp
import qrcode


ISSUER_NAME = "Cybersecurity AI Platform"


def generate_totp_secret():
    return pyotp.random_base32()


def build_totp_uri(email, secret):
    totp = pyotp.TOTP(secret)

    return totp.provisioning_uri(
        name=email,
        issuer_name=ISSUER_NAME
    )


def generate_totp_qr(email, secret):
    uri = build_totp_uri(
        email,
        secret
    )

    image = qrcode.make(uri)

    buffer = io.BytesIO()
    image.save(
        buffer,
        format="PNG"
    )

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


def verify_totp(secret, code):
    if not secret or not code:
        return False

    code = str(code).strip()

    if len(code) != 6 or not code.isdigit():
        return False

    totp = pyotp.TOTP(secret)

    return totp.verify(
        code,
        valid_window=1
    )
