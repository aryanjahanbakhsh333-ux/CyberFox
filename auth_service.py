from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models import User


def create_user(email, password):
    email = email.strip().lower()

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return None, "A user with this email already exists."

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        plan="free",
        role="user",
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    return user, None


def authenticate_user(email, password):
    email = email.strip().lower()

    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not user.is_active:
        return None

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return None

    user.last_login = datetime.utcnow()
    db.session.commit()

    return user
