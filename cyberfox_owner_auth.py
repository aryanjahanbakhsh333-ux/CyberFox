from __future__ import annotations

import os
import secrets
from functools import wraps
from typing import Optional

from flask import jsonify, session


# ============================================================
# CYBERFOX OWNER AUTHENTICATION
# ============================================================
#
# ACCESS MODEL
#
# Normal User:
#     WHITE HAT
#
# Owner:
#     WHITE HAT
#     GREY HAT
#     RED TEAM
#
# IMPORTANT:
# The browser NEVER decides who the owner is.
# Owner status comes from the trusted backend.
# ============================================================


ROLE_USER = "user"
ROLE_OWNER = "owner"


class CyberFoxOwnerAuth:

    def __init__(self):
        # Optional emergency/bootstrap owner ID.
        #
        # In production, the preferred source of truth is the
        # database role of the authenticated user.
        self.owner_user_id = os.getenv(
            "OWNER_USER_ID",
            ""
        ).strip()

        self.owner_email = os.getenv(
            "OWNER_EMAIL",
            ""
        ).strip().lower()

    # ========================================================
    # OWNER DETECTION
    # ========================================================

    def is_owner(
        self,
        *,
        user_id: Optional[str],
        email: Optional[str],
        database_role: Optional[str],
    ) -> bool:

        # ----------------------------------------------------
        # DATABASE ROLE
        # ----------------------------------------------------
        #
        # This is the preferred method.
        # If the trusted database says role=owner,
        # the user is Owner.
        # ----------------------------------------------------

        if database_role == ROLE_OWNER:
            return True

        # ----------------------------------------------------
        # OWNER USER ID
        # ----------------------------------------------------

        if (
            self.owner_user_id
            and user_id
            and secrets.compare_digest(
                str(user_id),
                str(self.owner_user_id)
            )
        ):
            return True

        # ----------------------------------------------------
        # OWNER EMAIL
        # ----------------------------------------------------
        #
        # This should only be used after the email belongs to
        # an authenticated account.
        # ----------------------------------------------------

        if (
            self.owner_email
            and email
            and secrets.compare_digest(
                email.lower(),
                self.owner_email
            )
        ):
            return True

        return False

    # ========================================================
    # GET CURRENT USER ROLE
    # ========================================================

    def get_role(
        self,
        *,
        user_id: Optional[str],
        email: Optional[str],
        database_role: Optional[str],
    ) -> str:

        if self.is_owner(
            user_id=user_id,
            email=email,
            database_role=database_role,
        ):
            return ROLE_OWNER

        return ROLE_USER

    # ========================================================
    # SECURITY MODES
    # ========================================================

    def allowed_modes(
        self,
        *,
        role: str
    ) -> list[str]:

        # Everyone gets White Hat.
        if role == ROLE_USER:
            return [
                "white_hat"
            ]

        # Only Owner gets Grey + Red.
        if role == ROLE_OWNER:
            return [
                "white_hat",
                "grey_hat",
                "red_team",
            ]

        # Unknown roles get the safest permission.
        return [
            "white_hat"
        ]

    # ========================================================
    # SESSION ROLE
    # ========================================================

    def set_authenticated_role(
        self,
        *,
        user_id: str,
        email: str,
        database_role: str,
    ) -> str:

        role = self.get_role(
            user_id=user_id,
            email=email,
            database_role=database_role,
        )

        # ----------------------------------------------------
        # Store ONLY the result determined by the backend.
        # ----------------------------------------------------

        session["cyberfox_user_id"] = str(user_id)
        session["cyberfox_role"] = role
        session["cyberfox_authenticated"] = True

        # Session marker helps prevent treating an arbitrary
        # client-side value as an authentication decision.
        session["cyberfox_auth_marker"] = secrets.token_urlsafe(32)

        return role

    # ========================================================
    # CURRENT ROLE
    # ========================================================

    @staticmethod
    def current_role() -> str:

        if not session.get("cyberfox_authenticated"):
            return ROLE_USER

        role = session.get(
            "cyberfox_role",
            ROLE_USER
        )

        # Never trust an unknown role.
        if role not in {
            ROLE_USER,
            ROLE_OWNER,
        }:
            return ROLE_USER

        return role

    # ========================================================
    # CURRENT USER ID
    # ========================================================

    @staticmethod
    def current_user_id() -> Optional[str]:

        if not session.get("cyberfox_authenticated"):
            return None

        user_id = session.get(
            "cyberfox_user_id"
        )

        if not user_id:
            return None

        return str(user_id)

    # ========================================================
    # OWNER CHECK
    # ========================================================

    @classmethod
    def current_user_is_owner(cls) -> bool:

        return cls.current_role() == ROLE_OWNER

    # ========================================================
    # OWNER-ONLY DECORATOR
    # ========================================================

    @classmethod
    def owner_required(cls, route_function):

        @wraps(route_function)
        def wrapper(*args, **kwargs):

            # ------------------------------------------------
            # Must be authenticated.
            # ------------------------------------------------

            if not session.get(
                "cyberfox_authenticated"
            ):
                return jsonify({
                    "ok": False,
                    "error": "authentication_required"
                }), 401

            # ------------------------------------------------
            # Must be Owner.
            # ------------------------------------------------

            if not cls.current_user_is_owner():
                return jsonify({
                    "ok": False,
                    "error": "owner_only",
                    "message": (
                        "This CyberFox feature is available "
                        "only to the verified site owner."
                    )
                }), 403

            return route_function(
                *args,
                **kwargs
            )

        return wrapper

    # ========================================================
    # MODE CHECK
    # ========================================================

    @classmethod
    def can_use_mode(
        cls,
        requested_mode: str
    ) -> bool:

        role = cls.current_role()

        allowed = cls.allowed_modes_for_role(
            role
        )

        return requested_mode in allowed

    @staticmethod
    def allowed_modes_for_role(
        role: str
    ) -> list[str]:

        if role == ROLE_OWNER:
            return [
                "white_hat",
                "grey_hat",
                "red_team",
            ]

        return [
            "white_hat"
        ]

    # ========================================================
    # SAFE MODE ENFORCEMENT
    # ========================================================

    @classmethod
    def enforce_mode(
        cls,
        requested_mode: str
    ) -> tuple[bool, str]:

        requested_mode = (
            requested_mode or "white_hat"
        ).lower().strip()

        allowed = cls.allowed_modes_for_role(
            cls.current_role()
        )

        if requested_mode not in {
            "white_hat",
            "grey_hat",
            "red_team",
        }:
            return False, "invalid_security_mode"

        if requested_mode not in allowed:

            return False, (
                "security_mode_not_available_for_this_user"
            )

        return True, "allowed"


# ============================================================
# GLOBAL INSTANCE
# ============================================================

cyberfox_owner_auth = CyberFoxOwnerAuth()


# ============================================================
# SIMPLE HELPERS
# ============================================================

def is_cyberfox_owner() -> bool:

    return CyberFoxOwnerAuth.current_user_is_owner()


def cyberfox_current_role() -> str:

    return CyberFoxOwnerAuth.current_role()


def cyberfox_allowed_modes() -> list[str]:

    return CyberFoxOwnerAuth.allowed_modes_for_role(
        CyberFoxOwnerAuth.current_role()
    )
