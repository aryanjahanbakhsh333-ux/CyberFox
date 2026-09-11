from datetime import datetime, timedelta


_ATTEMPTS = {}


def _get_key(identifier):
    return str(identifier).strip().lower()


def record_attempt(identifier):
    key = _get_key(identifier)

    now = datetime.utcnow()

    attempts = _ATTEMPTS.setdefault(
        key,
        []
    )

    attempts.append(now)

    return len(attempts)


def get_attempt_count(
    identifier,
    window_minutes=15
):
    key = _get_key(identifier)

    now = datetime.utcnow()

    cutoff = (
        now -
        timedelta(
            minutes=window_minutes
        )
    )

    attempts = _ATTEMPTS.get(
        key,
        []
    )

    valid_attempts = [
        item
        for item in attempts
        if item >= cutoff
    ]

    _ATTEMPTS[key] = valid_attempts

    return len(valid_attempts)


def is_rate_limited(
    identifier,
    maximum_attempts=5,
    window_minutes=15
):
    count = get_attempt_count(
        identifier,
        window_minutes
    )

    return count >= maximum_attempts


def clear_attempts(identifier):
    key = _get_key(identifier)

    _ATTEMPTS.pop(
        key,
        None
    )
