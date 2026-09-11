from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from database import db


def change_password(
    user,
    current_password,
    new_password
):
    if not check_password_hash(
        user.password_hash,
        current_password
    ):
        return False, "Current password is incorrect."

    if len(new_password) < 8:
        return False, (
            "New password must be at least 8 characters."
        )

    user.password_hash = generate_password_hash(
        new_password
    )

    db.session.commit()

    return True, None
