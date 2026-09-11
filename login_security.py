from datetime import datetime, timedelta

from rate_limiter import (
    is_rate_limited,
    record_attempt,
    clear_attempts
)

from security_config import SecurityConfig


def check_login_allowed(identifier):
    return not is_rate_limited(
        identifier,
        SecurityConfig.MAX_LOGIN_ATTEMPTS,
        SecurityConfig.LOGIN_LOCKOUT_MINUTES
    )


def register_failed_login(identifier):
    return record_attempt(
        identifier
    )


def register_successful_login(identifier):
    clear_attempts(
        identifier
    )


def get_lockout_message():
    return (
        "Too many failed login attempts. "
        "Please try again later."
    )
