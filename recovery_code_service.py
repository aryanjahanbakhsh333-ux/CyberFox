import hashlib
import secrets


RECOVERY_CODE_COUNT = 10
RECOVERY_CODE_LENGTH = 10


def _hash_code(code):
    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()


def generate_recovery_codes(
    count=RECOVERY_CODE_COUNT
):
    codes = []

    for _ in range(count):
        raw = secrets.token_hex(
            RECOVERY_CODE_LENGTH // 2
        )

        code = (
            raw[:5]
            + "-"
            + raw[5:10]
        )

        codes.append(code)

    return codes


def hash_recovery_codes(codes):
    return [
        _hash_code(code)
        for code in codes
    ]


def consume_recovery_code(
    code,
    hashed_codes
):
    if not code:
        return False, hashed_codes

    normalized = code.strip().lower()

    target_hash = _hash_code(
        normalized
    )

    remaining = list(hashed_codes)

    if target_hash not in remaining:
        return False, remaining

    remaining.remove(target_hash)

    return True, remaining
