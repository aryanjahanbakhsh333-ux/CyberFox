from password_policy import validate_password


def test_password_policy_rejects_short_password():
    result = validate_password("123")

    assert result["valid"] is False


def test_password_policy_rejects_digits_only():
    result = validate_password("12345678")

    assert result["valid"] is False


def test_password_policy_accepts_reasonable_password():
    result = validate_password(
        "SecurePassword123!"
    )

    assert result["valid"] is True
