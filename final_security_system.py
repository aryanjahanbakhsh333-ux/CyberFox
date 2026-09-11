import hashlib
import hmac
import secrets
import time
from functools import wraps

from flask import Blueprint, jsonify, request

from database import db
from models import User, SecurityEvent


security_final_api = Blueprint(
    "security_final_api",
    __name__,
    url_prefix="/api/security"
)


# --------------------------------------------------
# SESSION SECURITY
# --------------------------------------------------

SESSIONS = {}
SESSION_TTL = 60 * 60 * 24


def create_secure_session(user_id):
    token = secrets.token_urlsafe(48)

    SESSIONS[token] = {
        "user_id": user_id,
        "created": time.time(),
        "expires": time.time() + SESSION_TTL
    }

    return token


def get_secure_session(token):
    if not token:
        return None

    session = SESSIONS.get(token)

    if not session:
        return None

    if time.time() > session["expires"]:
        SESSIONS.pop(token, None)
        return None

    return session


def destroy_session(token):
    if token:
        SESSIONS.pop(token, None)


def current_user():
    header = request.headers.get("Authorization", "")

    if not header.startswith("Bearer "):
        return None

    token = header[7:].strip()

    session = get_secure_session(token)

    if not session:
        return None

    return User.query.get(session["user_id"])


def authentication_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        return function(user, *args, **kwargs)

    return wrapper


def owner_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        if user.role != "owner":
            return jsonify({
                "success": False,
                "error": "Owner access required."
            }), 403

        return function(user, *args, **kwargs)

    return wrapper


# --------------------------------------------------
# RATE LIMIT
# --------------------------------------------------

RATE_LIMIT = {}

MAX_REQUESTS = 60
WINDOW = 60


def rate_limited(identifier):

    now = time.time()

    history = RATE_LIMIT.get(identifier, [])

    history = [
        timestamp
        for timestamp in history
        if now - timestamp < WINDOW
    ]

    if len(history) >= MAX_REQUESTS:
        RATE_LIMIT[identifier] = history

        return True

    history.append(now)
    RATE_LIMIT[identifier] = history

    return False


# --------------------------------------------------
# SECURITY ANALYSIS
# --------------------------------------------------

def calculate_security_score(data):

    score = 100
    findings = []

    if data.get("weak_password"):
        score -= 25
        findings.append({
            "type": "weak_password",
            "severity": "high",
            "message": "Password security should be improved."
        })

    if data.get("missing_2fa"):
        score -= 20
        findings.append({
            "type": "missing_2fa",
            "severity": "medium",
            "message": "Two-factor authentication is not enabled."
        })

    if data.get("unknown_device"):
        score -= 20
        findings.append({
            "type": "unknown_device",
            "severity": "high",
            "message": "An unknown device requires verification."
        })

    if data.get("suspicious_activity"):
        score -= 25
        findings.append({
            "type": "suspicious_activity",
            "severity": "critical",
            "message": "Suspicious activity was detected."
        })

    if data.get("privacy_risk"):
        score -= 10
        findings.append({
            "type": "privacy_risk",
            "severity": "medium",
            "message": "Privacy settings should be reviewed."
        })

    score = max(0, min(100, score))

    if score >= 80:
        level = "low"
    elif score >= 60:
        level = "medium"
    elif score >= 40:
        level = "high"
    else:
        level = "critical"

    return {
        "score": score,
        "risk_level": level,
        "findings": findings
    }


def write_event(user_id, event_type, description, severity="info"):

    event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        description=description,
        severity=severity
    )

    db.session.add(event)
    db.session.commit()

    return event


@security_final_api.post("/analyze")
@authentication_required
def analyze(user):

    identifier = f"user:{user.id}"

    if rate_limited(identifier):
        return jsonify({
            "success": False,
            "error": "Too many requests."
        }), 429

    data = request.get_json(silent=True) or {}

    result = calculate_security_score(data)

    write_event(
        user.id,
        "security_analysis",
        f"Security analysis completed. Score: {result['score']}",
        result["risk_level"]
    )

    return jsonify({
        "success": True,
        "security": result
    })


@security_final_api.get("/events")
@authentication_required
def events(user):

    rows = (
        SecurityEvent.query
        .filter_by(user_id=user.id)
        .order_by(SecurityEvent.created_at.desc())
        .limit(100)
        .all()
    )

    return jsonify({
        "success": True,
        "events": [
            {
                "id": event.id,
                "type": event.event_type,
                "description": event.description,
                "severity": event.severity,
                "created_at": (
                    event.created_at.isoformat()
                    if event.created_at
                    else None
                )
            }
            for event in rows
        ]
    })


def register_security_final(app):
    app.register_blueprint(security_final_api)
