from __future__ import annotations

import hashlib
import os
import secrets
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ============================================================
# CYBERFOX CORE
# ============================================================
#
# USER:
#   WHITE HAT
#
# OWNER:
#   WHITE HAT + GREY HAT + RED TEAM
#
# Grey/Red are restricted to authorized assets/labs.
# Credentials are NEVER stored by this module.
# Device access requires explicit user consent.
# ============================================================


class Role(str, Enum):
    USER = "user"
    OWNER = "owner"


class SecurityMode(str, Enum):
    WHITE_HAT = "white_hat"
    GREY_HAT = "grey_hat"
    RED_TEAM = "red_team"


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConsentStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class User:
    user_id: str
    email: str
    role: Role = Role.USER
    created_at: float = field(default_factory=time.time)


@dataclass
class DeviceConsent:
    consent_id: str
    user_id: str
    device_id: str

    # What the user explicitly approved.
    permissions: set[str]

    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0

    status: ConsentStatus = ConsentStatus.ACTIVE

    # Never store passwords, authentication tokens,
    # recovery codes, private keys or raw payment data.
    stores_credentials: bool = False


@dataclass
class SecurityFinding:
    category: str
    severity: Risk
    title: str
    description: str
    recommendation: str


@dataclass
class SecurityReport:
    device_id: str
    score: int
    findings: list[SecurityFinding]
    generated_at: float = field(default_factory=time.time)


# ============================================================
# CYBERFOX OWNER CONFIGURATION
# ============================================================

class OwnerRegistry:

    def __init__(self) -> None:
        self.owner_user_id = os.getenv(
            "OWNER_USER_ID",
            ""
        ).strip()

        self.owner_email = os.getenv(
            "OWNER_EMAIL",
            ""
        ).strip().lower()

    def is_owner(self, user: User) -> bool:

        # Database role is the primary source of truth.
        if user.role == Role.OWNER:
            return True

        # Optional bootstrap protection.
        if (
            self.owner_user_id
            and secrets.compare_digest(
                str(user.user_id),
                self.owner_user_id
            )
        ):
            return True

        if (
            self.owner_email
            and secrets.compare_digest(
                user.email.lower(),
                self.owner_email
            )
        ):
            return True

        return False


# ============================================================
# SECURITY ACCESS
# ============================================================

class SecurityAccess:

    USER_MODES = {
        SecurityMode.WHITE_HAT
    }

    OWNER_MODES = {
        SecurityMode.WHITE_HAT,
        SecurityMode.GREY_HAT,
        SecurityMode.RED_TEAM
    }

    @classmethod
    def allowed_modes(cls, user: User) -> set[SecurityMode]:

        if user.role == Role.OWNER:
            return cls.OWNER_MODES.copy()

        return cls.USER_MODES.copy()

    @classmethod
    def can_use_mode(
        cls,
        user: User,
        mode: SecurityMode
    ) -> bool:

        return mode in cls.allowed_modes(user)

    @classmethod
    def require_authorized_scope(
        cls,
        user: User,
        mode: SecurityMode,
        authorized_asset: bool,
        laboratory: bool
    ) -> bool:

        # White Hat defensive assistance.
        if mode == SecurityMode.WHITE_HAT:
            return True

        # Grey/Red are Owner-only.
        if user.role != Role.OWNER:
            return False

        # Advanced testing requires an authorized scope.
        return authorized_asset or laboratory


# ============================================================
# PRIVACY-FIRST DEVICE ACCESS
# ============================================================

class DevicePrivacy:

    SAFE_PERMISSIONS = {
        "security_scan",
        "installed_app_security_review",
        "network_security_review",
        "privacy_scan",
        "storage_security_review",
        "malware_indicators",
        "security_configuration",
        "security_report"
    }

    DANGEROUS_DATA = {
        "password",
        "passwords",
        "authentication_token",
        "session_token",
        "private_key",
        "recovery_code",
        "credit_card",
        "bank_password"
    }

    @classmethod
    def create_consent(
        cls,
        user: User,
        device_id: str,
        permissions: set[str],
        duration_seconds: int = 3600
    ) -> DeviceConsent:

        clean_permissions = {
            permission
            for permission in permissions
            if permission in cls.SAFE_PERMISSIONS
        }

        return DeviceConsent(
            consent_id=secrets.token_urlsafe(32),
            user_id=user.user_id,
            device_id=device_id,
            permissions=clean_permissions,
            expires_at=time.time() + duration_seconds,
            status=ConsentStatus.ACTIVE,
            stores_credentials=False
        )

    @classmethod
    def is_valid(
        cls,
        consent: DeviceConsent
    ) -> bool:

        if consent.status != ConsentStatus.ACTIVE:
            return False

        if time.time() >= consent.expires_at:
            consent.status = ConsentStatus.EXPIRED
            return False

        return True

    @classmethod
    def has_permission(
        cls,
        consent: DeviceConsent,
        permission: str
    ) -> bool:

        return (
            cls.is_valid(consent)
            and permission in consent.permissions
        )

    @staticmethod
    def revoke(consent: DeviceConsent) -> None:
        consent.status = ConsentStatus.REVOKED


# ============================================================
# DEVICE SECURITY SCANNER
# ============================================================

class DeviceSecurityScanner:

    def scan(
        self,
        device_id: str,
        consent: DeviceConsent,
        device_data: dict[str, Any]
    ) -> SecurityReport:

        if not DevicePrivacy.has_permission(
            consent,
            "security_scan"
        ):
            raise PermissionError(
                "The user has not authorized a security scan."
            )

        findings: list[SecurityFinding] = []

        # ----------------------------------------------------
        # Example defensive checks.
        # The actual mobile agent must provide real device data.
        # ----------------------------------------------------

        if device_data.get("security_updates_missing"):
            findings.append(
                SecurityFinding(
                    category="system",
                    severity=Risk.HIGH,
                    title="Security updates are missing",
                    description=(
                        "The device appears to be missing important "
                        "security updates."
                    ),
                    recommendation=(
                        "Install the latest official operating-system "
                        "security updates."
                    )
                )
            )

        if device_data.get("suspicious_app"):
            findings.append(
                SecurityFinding(
                    category="malware",
                    severity=Risk.HIGH,
                    title="Suspicious application detected",
                    description=(
                        "A potentially unsafe application was reported "
                        "by the device security agent."
                    ),
                    recommendation=(
                        "Review the application and remove it using "
                        "the official device controls if confirmed unsafe."
                    )
                )
            )

        if device_data.get("unknown_profile"):
            findings.append(
                SecurityFinding(
                    category="configuration",
                    severity=Risk.MEDIUM,
                    title="Unknown configuration profile",
                    description=(
                        "An unfamiliar configuration profile was reported."
                    ),
                    recommendation=(
                        "Review the profile in the device's official "
                        "security/settings interface."
                    )
                )
            )

        if device_data.get("weak_security_configuration"):
            findings.append(
                SecurityFinding(
                    category="configuration",
                    severity=Risk.MEDIUM,
                    title="Security configuration needs improvement",
                    description=(
                        "Some recommended security controls appear "
                        "to be disabled or weak."
                    ),
                    recommendation=(
                        "Enable supported security protections and MFA."
                    )
                )
            )

        score = self.calculate_score(findings)

        return SecurityReport(
            device_id=device_id,
            score=score,
            findings=findings
        )

    @staticmethod
    def calculate_score(
        findings: list[SecurityFinding]
    ) -> int:

        score = 100

        penalties = {
            Risk.LOW: 5,
            Risk.MEDIUM: 10,
            Risk.HIGH: 20,
            Risk.CRITICAL: 40
        }

        for finding in findings:
            score -= penalties[finding.severity]

        return max(0, min(100, score))


# ============================================================
# SAFE DEVICE REPAIR PLANNER
# ============================================================

class DeviceRepairPlanner:

    SAFE_ACTIONS = {
        "update_os",
        "remove_confirmed_malicious_app",
        "disable_suspicious_profile",
        "reset_security_configuration",
        "enable_mfa",
        "review_permissions",
        "clear_malicious_browser_data"
    }

    @classmethod
    def create_plan(
        cls,
        report: SecurityReport
    ) -> list[dict[str, Any]]:

        plan = []

        for finding in report.findings:

            action = None

            if finding.category == "malware":
                action = "remove_confirmed_malicious_app"

            elif finding.category == "system":
                action = "update_os"

            elif finding.category == "configuration":
                action = "review_permissions"

            if action in cls.SAFE_ACTIONS:
                plan.append({
                    "action": action,
                    "requires_user_confirmation": True,
                    "reason": finding.title
                })

        return plan


# ============================================================
# LEGAL ACCOUNT RECOVERY
# ============================================================

class LegalRecovery:

    ALLOWED_PROVIDERS = {
        "instagram",
        "whatsapp",
        "google",
        "apple",
        "microsoft"
    }

    @classmethod
    def create_recovery_plan(
        cls,
        provider: str
    ) -> dict[str, Any]:

        provider = provider.lower().strip()

        if provider not in cls.ALLOWED_PROVIDERS:
            raise ValueError(
                "Unsupported recovery provider."
            )

        return {
            "provider": provider,
            "method": "official_recovery",
            "credentials_collected": False,
            "credential_storage": False,
            "steps": [
                "open_official_recovery_flow",
                "verify_account_ownership",
                "reset_credentials_through_provider",
                "enable_mfa",
                "review_active_sessions"
            ]
        }


# ============================================================
# AI SECURITY BRAIN
# ============================================================

class CyberFoxSecurityBrain:

    BLOCKED_REQUESTS = (
        "credential theft",
        "steal password",
        "steal passwords",
        "account takeover",
        "session theft",
        "token theft",
        "authentication bypass",
        "unauthorized access",
        "ransomware",
        "deploy malware",
        "keylogger",
        "data exfiltration",
        "real world phishing"
    )

    @classmethod
    def analyze(
        cls,
        user: User,
        message: str,
        mode: SecurityMode,
        authorized_asset: bool = False,
        laboratory: bool = False
    ) -> dict[str, Any]:

        message_lower = message.lower()

        # Always reject explicitly harmful requests.
        if any(
            pattern in message_lower
            for pattern in cls.BLOCKED_REQUESTS
        ):
            return {
                "allowed": False,
                "mode": mode.value,
                "risk": Risk.CRITICAL.value,
                "reason": (
                    "This request involves credential theft, "
                    "unauthorized access, malware, or another "
                    "prohibited operation."
                )
            }

        # Check role-based mode access.
        if not SecurityAccess.can_use_mode(
            user,
            mode
        ):
            return {
                "allowed": False,
                "mode": mode.value,
                "risk": Risk.HIGH.value,
                "reason": (
                    "This security mode is restricted to "
                    "the CyberFox Owner."
                )
            }

        # Grey/Red require authorized scope.
        if not SecurityAccess.require_authorized_scope(
            user,
            mode,
            authorized_asset,
            laboratory
        ):
            return {
                "allowed": False,
                "mode": mode.value,
                "risk": Risk.HIGH.value,
                "reason": (
                    "Advanced testing requires an authorized "
                    "asset or controlled laboratory."
                )
            }

        return {
            "allowed": True,
            "mode": mode.value,
            "risk": Risk.LOW.value,
            "role": user.role.value,
            "reason": "Request is within CyberFox security scope."
        }


# ============================================================
# CYBERFOX PLATFORM
# ============================================================

class CyberFox:

    def __init__(self):

        self.owner_registry = OwnerRegistry()

        self.users: dict[str, User] = {}

        self.consents: dict[str, DeviceConsent] = {}

        self.scanner = DeviceSecurityScanner()

        self.brain = CyberFoxSecurityBrain()

    # ========================================================
    # USER
    # ========================================================

    def register_user(
        self,
        user_id: str,
        email: str
    ) -> User:

        user = User(
            user_id=user_id,
            email=email,
            role=Role.USER
        )

        self.users[user_id] = user

        return user

    # ========================================================
    # OWNER
    # ========================================================

    def authenticate_owner(
        self,
        user_id: str
    ) -> User:

        user = self.users.get(user_id)

        if user is None:
            raise PermissionError(
                "User does not exist."
            )

        if not self.owner_registry.is_owner(user):
            raise PermissionError(
                "This account is not the CyberFox Owner."
            )

        # Normalize the trusted backend role.
        user.role = Role.OWNER

        return user

    # ========================================================
    # DEVICE CONSENT
    # ========================================================

    def grant_device_consent(
        self,
        user_id: str,
        device_id: str,
        permissions: set[str],
        duration_seconds: int = 3600
    ) -> DeviceConsent:

        user = self.users.get(user_id)

        if user is None:
            raise PermissionError(
                "User authentication required."
            )

        consent = DevicePrivacy.create_consent(
            user=user,
            device_id=device_id,
            permissions=permissions,
            duration_seconds=duration_seconds
        )

        self.consents[consent.consent_id] = consent

        return consent

    # ========================================================
    # REVOKE DEVICE ACCESS
    # ========================================================

    def revoke_device_consent(
        self,
        user_id: str,
        consent_id: str
    ) -> None:

        consent = self.consents.get(consent_id)

        if consent is None:
            raise ValueError(
                "Consent does not exist."
            )

        if consent.user_id != user_id:
            raise PermissionError(
                "You cannot revoke another user's consent."
            )

        DevicePrivacy.revoke(consent)

    # ========================================================
    # DEVICE SCAN
    # ========================================================

    def scan_device(
        self,
        user_id: str,
        consent_id: str,
        device_data: dict[str, Any]
    ) -> SecurityReport:

        consent = self.consents.get(consent_id)

        if consent is None:
            raise PermissionError(
                "Device consent not found."
            )

        if consent.user_id != user_id:
            raise PermissionError(
                "This consent belongs to another user."
            )

        if not DevicePrivacy.has_permission(
            consent,
            "security_scan"
        ):
            raise PermissionError(
                "Security scan was not authorized."
            )

        return self.scanner.scan(
            device_id=consent.device_id,
            consent=consent,
            device_data=device_data
        )

    # ========================================================
    # SECURITY AI
    # ========================================================

    def security_ai(
        self,
        user_id: str,
        message: str,
        mode: SecurityMode = SecurityMode.WHITE_HAT,
        authorized_asset: bool = False,
        laboratory: bool = False
    ) -> dict[str, Any]:

        user = self.users.get(user_id)

        if user is None:
            raise PermissionError(
                "Authentication required."
            )

        return self.brain.analyze(
            user=user,
            message=message,
            mode=mode,
            authorized_asset=authorized_asset,
            laboratory=laboratory
        )


# ============================================================
# SECURITY UTILITY
# ============================================================

def hash_identifier(value: str) -> str:
    """
    Hash a non-secret identifier when a pseudonymous reference
    is needed.

    Do NOT use this as a password hashing function.
    """

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


# ============================================================
# EXAMPLE
# ============================================================

if __name__ == "__main__":

    cyberfox = CyberFox()

    # --------------------------------------------------------
    # Normal user
    # --------------------------------------------------------

    user = cyberfox.register_user(
        user_id="user-001",
        email="user@example.com"
    )

    print(
        "USER MODES:",
        [
            mode.value
            for mode in SecurityAccess.allowed_modes(user)
        ]
    )

    # --------------------------------------------------------
    # Owner
    # --------------------------------------------------------

    owner = cyberfox.register_user(
        user_id=os.getenv(
            "OWNER_USER_ID",
            "owner-demo"
        ),
        email=os.getenv(
            "OWNER_EMAIL",
            "owner@example.com"
        )
    )

    try:
        owner = cyberfox.authenticate_owner(
            owner.user_id
        )

        print(
            "OWNER MODES:",
            [
                mode.value
                for mode in SecurityAccess.allowed_modes(owner)
            ]
        )

    except PermissionError as error:

        print(
            "OWNER AUTHENTICATION:",
            str(error)
        )

    # --------------------------------------------------------
    # User device consent
    # --------------------------------------------------------

    consent = cyberfox.grant_device_consent(
        user_id=user.user_id,
        device_id="device-001",
        permissions={
            "security_scan",
            "privacy_scan",
            "malware_indicators",
            "security_report"
        },
        duration_seconds=3600
    )

    print(
        "DEVICE CONSENT:",
        consent.consent_id
    )

    # --------------------------------------------------------
    # Defensive device scan
    # --------------------------------------------------------

    report = cyberfox.scan_device(
        user_id=user.user_id,
        consent_id=consent.consent_id,
        device_data={
            "security_updates_missing": True,
            "suspicious_app": False,
            "unknown_profile": False,
            "weak_security_configuration": True
        }
    )

    print(
        "SECURITY SCORE:",
        report.score
    )

    # --------------------------------------------------------
    # AI test
    # --------------------------------------------------------

    result = cyberfox.security_ai(
        user_id=user.user_id,
        message="چطور امنیت گوشی خودم را بهتر کنم؟",
        mode=SecurityMode.WHITE_HAT
    )

    print(
        "AI RESULT:",
        result
    )
