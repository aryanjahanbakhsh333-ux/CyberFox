def validate_password(password):
    if not isinstance(password, str):
        return False, "Invalid password."

    if len(password) < 8:
        return False, (
            "Password must be at least 8 characters."
        )

    if password.isdigit():
        return False, (
            "Password cannot contain only numbers."
        )

    if password.isalpha():
        return False, (
            "Password should contain numbers "
            "or symbols."
        )

    return True, None
