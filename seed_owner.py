import os

from app_factory import create_app
from database import db
from models import User

from werkzeug.security import generate_password_hash


app = create_app()


with app.app_context():
    owner_email = os.getenv(
        "OWNER_EMAIL",
        ""
    ).strip().lower()

    owner_password = os.getenv(
        "OWNER_INITIAL_PASSWORD",
        ""
    )

    if not owner_email or not owner_password:
        raise RuntimeError(
            "OWNER_EMAIL and OWNER_INITIAL_PASSWORD "
            "must be configured."
        )

    owner = User.query.filter_by(
        email=owner_email
    ).first()

    if owner:
        owner.role = "owner"
        owner.is_active = True
        db.session.commit()

        print("Existing user promoted to owner.")
    else:
        owner = User(
            email=owner_email,
            password_hash=generate_password_hash(
                owner_password
            ),
            plan="pro",
            role="owner",
            is_active=True
        )

        db.session.add(owner)
        db.session.commit()

        print("Owner account created.")
