import time

from redis_store import redis_store


def is_rate_limited(
    key,
    limit,
    window_seconds
):
    redis_key = f"rate:{key}"

    current = redis_store.get(
        redis_key
    )

    now = int(time.time())

    if not current:
        redis_store.set(
            redis_key,
            {
                "count": 1,
                "started": now
            },
            window_seconds
        )

        return False

    if now - current["started"] >= window_seconds:
        redis_store.set(
            redis_key,
            {
                "count": 1,
                "started": now
            },
            window_seconds
        )

        return False

    if current["count"] >= limit:
        return True

    current["count"] += 1

    remaining = max(
        1,
        window_seconds
        - (now - current["started"])
    )

    redis_store.set(
        redis_key,
        current,
        remaining
    )

    return False
