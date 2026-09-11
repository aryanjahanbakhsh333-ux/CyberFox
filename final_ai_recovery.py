import re
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from models import User
from database import db

from final_security_system import (
    current_user,
    authentication_required
)


ai_recovery_api = Blueprint(
    "ai_recovery_api",
    __name__,
    url_prefix="/api/ai"
)


# --------------------------------------------------
# AI SECURITY ENGINE
# --------------------------------------------------

def analyze_threat(data):

    signals = {
        "suspicious_activity": bool(
            data.get("suspicious_activity")
        ),
        "unknown_device": bool(
            data.get("unknown_device")
        ),
        "weak_password": bool(
            data.get("weak_password")
        ),
        "missing_2fa": bool(
            data.get("missing_2fa")
        ),
        "privacy_risk": bool(
            data.get("privacy_risk")
        )
    }

    weights = {
        "suspicious_activity": 35,
        "unknown_device": 25,
        "weak_password": 15,
        "missing_2fa": 15,
        "privacy_risk": 10
    }

    risk = sum(
        weights[key]
        for key, value in signals.items()
        if value
    )

    risk = min(100, risk)

    if risk >= 75:
        level = "critical"
    elif risk >= 50:
        level = "high"
    elif risk >= 25:
        level = "medium"
    else:
        level = "low"

    recommendations = []

    if signals["weak_password"]:
        recommendations.append(
            "Change the password to a unique strong password."
        )

    if signals["missing_2fa"]:
        recommendations.append(
            "Enable two-factor authentication."
        )

    if signals["unknown_device"]:
        recommendations.append(
            "Review and remove unknown sessions or devices."
        )

    if signals["suspicious_activity"]:
        recommendations.append(
            "Review recent account activity immediately."
        )

    if signals["privacy_risk"]:
        recommendations.append(
            "Review privacy and connected-app permissions."
        )

    return {
        "risk_score": risk,
        "risk_level": level,
        "signals": signals,
        "recommendations": recommendations
    }


# --------------------------------------------------
# LEGAL ACCOUNT RECOVERY
# --------------------------------------------------

RECOVERY_CODES = {}

RECOVERY_EXPIRY = timedelta(minutes=15)


def create_recovery_code(user_id):

    code = f"{__import__('secrets').randbelow(1000000):06d}"

    RECOVERY_CODES[user_id] = {
        "code": code,
        "expires": datetime.utcnow() + RECOVERY_EXPIRY
    }

    return code


def verify_recovery_code(user_id, code):

    record = RECOVERY_CODES.get(user_id)

    if not record:
        return False

    if datetime.utcnow() > record["expires"]:
        RECOVERY_CODES.pop(user_id, None)
        return False

    valid = code == record["code"]

    if valid:
        RECOVERY_CODES.pop(user_id, None)

    return valid


def recovery_allowed(user):

    return bool(
        user
        and user.is_active
    )


# --------------------------------------------------
# PASSWORD RECOVERY
# --------------------------------------------------

def validate_password(password):

    if not isinstance(password, str):
        return False

    if len(password) < 12:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


@ai_recovery_api.post("/threat-analysis")
@authentication_required
def threat_analysis(user):

    data = request.get_json(silent=True) or {}

    result = analyze_threat(data)

    return jsonify({
        "success": True,
        "analysis": result
    })


@ai_recovery_api.post("/recovery/start")
@authentication_required
def start_recovery(user):

    if not recovery_allowed(user):
        return jsonify({
            "success": False,
            "error": "Recovery is unavailable."
        }), 403

    code = create_recovery_code(user.id)

    # In production this code must be delivered
    # through a verified email/SMS provider.
    return jsonify({
        "success": True,
        "message": (
            "Recovery verification started."
        ),
        "verification_required": True,
        "development_code": code
    })


@ai_recovery_api.post("/recovery/verify")
@authentication_required
def verify_recovery(user):

    data = request.get_json(silent=True) or {}

    code = str(data.get("code", "")).strip()

    if not verify_recovery_code(user.id, code):
        return jsonify({
            "success": False,
            "error": "Invalid or expired verification code."
        }), 400

    return jsonify({
        "success": True,
        "verified": True,
        "message": (
            "Identity verification completed."
        )
    })


@ai_recovery_api.post("/password/check")
@authentication_required
def password_check(user):

    data = request.get_json(silent=True) or {}

    password = data.get("password", "")

    return jsonify({
        "success": True,
        "strong": validate_password(password)
    })


# --------------------------------------------------
# IMPORTANT SAFETY BOUNDARY
# --------------------------------------------------

def official_recovery_only():

    return {
        "allowed": True,
        "methods": [
            "verified_identity",
            "official_account_recovery",
            "verified_email",
            "verified_phone",
            "trusted_device"
        ],
        "blocked": [
            "password_guessing",
            "brute_force",
            "credential_extraction",
            "lock_bypass",
            "authentication_bypass"
        ]
    }


@ai_recovery_api.get("/recovery/policy")
def recovery_policy():

    return jsonify({
        "success": True,
        "policy": official_recovery_only()
    })


def register_ai_recovery(app):
    app.register_blueprint(ai_recovery_api)
