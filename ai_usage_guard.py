from datetime import datetime, timedelta


class AIUsageGuard:
    def __init__(
        self,
        free_limit=20,
        pro_limit=500
    ):
        self.free_limit = free_limit
        self.pro_limit = pro_limit
        self.usage = {}

    def _key(self, user_id):
        return str(user_id)

    def _reset_if_needed(self, user_id):
        key = self._key(user_id)
        now = datetime.utcnow()

        record = self.usage.get(key)

        if not record:
            self.usage[key] = {
                "count": 0,
                "started": now
            }
            return

        if now - record["started"] >= timedelta(
            hours=24
        ):
            self.usage[key] = {
                "count": 0,
                "started": now
            }

    def allowed(self, user_id, plan):
        self._reset_if_needed(user_id)

        record = self.usage[
            self._key(user_id)
        ]

        limit = (
            self.pro_limit
            if plan == "pro"
            else self.free_limit
        )

        return record["count"] < limit

    def consume(self, user_id, plan):
        if not self.allowed(
            user_id,
            plan
        ):
            return False

        key = self._key(user_id)

        self.usage[key]["count"] += 1

        return True

    def status(self, user_id, plan):
        self._reset_if_needed(user_id)

        record = self.usage[
            self._key(user_id)
        ]

        limit = (
            self.pro_limit
            if plan == "pro"
            else self.free_limit
        )

        return {
            "used": record["count"],
            "limit": limit,
            "remaining": max(
                0,
                limit - record["count"]
            )
        }
