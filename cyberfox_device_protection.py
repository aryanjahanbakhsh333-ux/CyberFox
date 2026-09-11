from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ============================================================
# CYBERFOX DEVICE PROTECTION
# ============================================================
#
# USER:
#   WHITE HAT ONLY
#
# OWNER:
#   WHITE HAT + GREY HAT + RED TEAM
#
# PRIVACY:
#   - Never stores raw passwords
#   - Never stores authentication tokens
#   - Never stores recovery codes
#   - Never stores private keys
#   - Device access requires explicit consent
#   - Consent can expire or be revoked
#
# IMPORTANT:
# This module is a backend security engine.
# Real device repair requires a CyberFox mobile/desktop agent
# with explicit user permission and OS-supported capabilities.
# ============================================================


class ConsentStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RepairStatus(str, Enum):
    RECOMMENDED = "recommended"
    WAITING_FOR_CONFIRMATION = "waiting_for_confirmation"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================
# PRIVACY RULES
# ============================================================

FORBIDDEN_DATA_FIELDS = {
    "password",
    "passwords",
    "raw_password",
    "authentication_token",
    "auth_token",
    "access_token",
    "refresh_token",
    "session_token",
    "cookie",
    "session_cookie",
    "private_key",
    "recovery_code",
    "backup_code",
    "credit_card_number",
    "cvv",
    "bank_password",
}


ALLOWED_DEVICE_PERMISSIONS = {
    "security_scan",
    "malware_scan",
    "installed_apps",
    "app_security",
    "security_configuration",
    "network_security",
    "privacy_scan",
    "browser_security",
    "device_integrity",
    "storage_security",
    "security_report",
}


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class DeviceConsent:
    consent_id: str
    user_id: str
    device_id: str

    permissions: set[str]

    created_at: float
    expires_at: float

    status: ConsentStatus = ConsentStatus.ACTIVE

    # Always False by design.
    stores_credentials: bool = False


@dataclass
class DeviceFinding:
    finding_id: str
    category: str
    severity: Severity
    title: str
    description: str

    recommended_action: str

    requires_user_confirmation: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceSecurityReport:
    report_id: str
    user_id: str
    device_id: str

    score: int

    findings: list[DeviceFinding]

    created_at: float = field(default_factory=time.time)


@dataclass
class RepairAction:
    action_id: str
    report_id: str
    device_id: str

    action: str
    reason: str

    status: RepairStatus = (
        RepairStatus.WAITING_FOR_CONFIRMATION
    )

    requires_user_confirmation: bool = True

    created_at: float = field(default_factory=time.time)

    approved_at: float | None = None
    completed_at: float | None = None


# ============================================================
# PRIVACY GUARD
# ============================================================

class PrivacyGuard:
    """
    Prevents CyberFox from accidentally accepting sensitive
    credentials or authentication material.
    """

    @staticmethod
    def sanitize_device_data(
        data: dict[str, Any]
    ) -> dict[str, Any]:

        clean: dict[str, Any] = {}

        for key, value in data.items():

            normalized = (
                str(key)
                .strip()
                .lower()
                .replace("-", "_")
            )

            if normalized in FORBIDDEN_DATA_FIELDS:
                continue

            # Also block obvious credential-like field names.
            if any(
                blocked in normalized
                for blocked in (
                    "password",
                    "token",
                    "private_key",
                    "recovery_code",
                    "secret_key",
                    "session_cookie",
                )
            ):
                continue

            clean[key] = value

        return clean

    @staticmethod
    def contains_forbidden_data(
        data: dict[str, Any]
    ) -> bool:

        for key in data.keys():

            normalized = (
                str(key)
                .strip()
                .lower()
                .replace("-", "_")
            )

            if normalized in FORBIDDEN_DATA_FIELDS:
                return True

            if any(
                blocked in normalized
                for blocked in (
                    "password",
                    "token",
                    "private_key",
                    "recovery_code",
                    "session_cookie",
                )
            ):
                return True

        return False


# ============================================================
# CONSENT MANAGER
# ============================================================

class DeviceConsentManager:

    @staticmethod
    def create_consent(
        user_id: str,
        device_id: str,
        permissions: set[str],
        duration_seconds: int = 3600,
    ) -> DeviceConsent:

        if not user_id:
            raise ValueError("user_id is required.")

        if not device_id:
            raise ValueError("device_id is required.")

        if duration_seconds <= 0:
            raise ValueError(
                "Consent duration must be positive."
            )

        clean_permissions = (
            permissions & ALLOWED_DEVICE_PERMISSIONS
        )

        if not clean_permissions:
            raise ValueError(
                "No valid device permissions were requested."
            )

        now = time.time()

        return DeviceConsent(
            consent_id=secrets.token_urlsafe(32),
            user_id=user_id,
            device_id=device_id,
            permissions=clean_permissions,
            created_at=now,
            expires_at=now + duration_seconds,
            status=ConsentStatus.ACTIVE,
            stores_credentials=False,
        )

    @staticmethod
    def is_valid(
        consent: DeviceConsent,
        user_id: str,
        device_id: str,
        permission: str,
    ) -> bool:

        if consent.user_id != user_id:
            return False

        if consent.device_id != device_id:
            return False

        if consent.status != ConsentStatus.ACTIVE:
            return False

        if time.time() >= consent.expires_at:
            consent.status = ConsentStatus.EXPIRED
            return False

        return permission in consent.permissions

    @staticmethod
    def revoke(
        consent: DeviceConsent
    ) -> None:

        consent.status = ConsentStatus.REVOKED


# ============================================================
# DEVICE SECURITY SCANNER
# ============================================================

class CyberFoxDeviceScanner:

    SEVERITY_PENALTY = {
        Severity.INFO: 0,
        Severity.LOW: 5,
        Severity.MEDIUM: 10,
        Severity.HIGH: 20,
        Severity.CRITICAL: 40,
    }

    def scan(
        self,
        user_id: str,
        device_id: str,
        consent: DeviceConsent,
        device_data: dict[str, Any],
    ) -> DeviceSecurityReport:

        if not DeviceConsentManager.is_valid(
            consent=consent,
            user_id=user_id,
            device_id=device_id,
            permission="security_scan",
        ):
            raise PermissionError(
                "A valid user-approved security scan "
                "permission is required."
            )

        # Never process credentials.
        safe_data = PrivacyGuard.sanitize_device_data(
            device_data
        )

        findings: list[DeviceFinding] = []

        # ----------------------------------------------------
        # OPERATING SYSTEM
        # ----------------------------------------------------

        if safe_data.get("security_updates_missing"):

            findings.append(
                self._finding(
                    category="system",
                    severity=Severity.HIGH,
                    title="Security updates are missing",
                    description=(
                        "The device reports missing operating-system "
                        "security updates."
                    ),
                    action="update_os",
                )
            )

        # ----------------------------------------------------
        # MALWARE / SUSPICIOUS APP
        # ----------------------------------------------------

        if safe_data.get("suspicious_app"):

            findings.append(
                self._finding(
                    category="malware",
                    severity=Severity.HIGH,
                    title="Suspicious application detected",
                    description=(
                        "The device agent reported an application "
                        "that requires security review."
                    ),
                    action="review_or_remove_confirmed_malicious_app",
                )
            )

        if safe_data.get("confirmed_malicious_app"):

            findings.append(
                self._finding(
                    category="malware",
                    severity=Severity.CRITICAL,
                    title="Confirmed malicious application",
                    description=(
                        "The device agent reports an application "
                        "confirmed as malicious."
                    ),
                    action="remove_confirmed_malicious_app",
                )
            )

        # ----------------------------------------------------
        # CONFIGURATION
        # ----------------------------------------------------

        if safe_data.get("unknown_profile"):

            findings.append(
                self._finding(
                    category="configuration",
                    severity=Severity.HIGH,
                    title="Unknown configuration profile",
                    description=(
                        "An unfamiliar device configuration profile "
                        "was reported."
                    ),
                    action="review_and_disable_profile",
                )
            )

        if safe_data.get("weak_security_configuration"):

            findings.append(
                self._finding(
                    category="configuration",
                    severity=Severity.MEDIUM,
                    title="Security configuration needs improvement",
                    description=(
                        "Some recommended security protections "
                        "appear to be disabled."
                    ),
                    action="strengthen_security_configuration",
                )
            )

        # ----------------------------------------------------
        # NETWORK
        # ----------------------------------------------------

        if safe_data.get("unsafe_network"):

            findings.append(
                self._finding(
                    category="network",
                    severity=Severity.MEDIUM,
                    title="Potentially unsafe network",
                    description=(
                        "The device reports a network condition "
                        "that may increase security risk."
                    ),
                    action="review_network_security",
                )
            )

        # ----------------------------------------------------
        # PRIVACY
        # ----------------------------------------------------

        if safe_data.get("excessive_permissions"):

            findings.append(
                self._finding(
                    category="privacy",
                    severity=Severity.MEDIUM,
                    title="Excessive application permissions",
                    description=(
                        "Some applications appear to have "
                        "permissions that may not be necessary."
                    ),
                    action="review_app_permissions",
                )
            )

        # ----------------------------------------------------
        # BROWSER
        # ----------------------------------------------------

        if safe_data.get("malicious_browser_data"):

            findings.append(
                self._finding(
                    category="browser",
                    severity=Severity.HIGH,
                    title="Suspicious browser data detected",
                    description=(
                        "The device agent reported potentially "
                        "malicious browser data."
                    ),
                    action="clear_confirmed_malicious_browser_data",
                )
            )

        score = self.calculate_score(findings)

        return DeviceSecurityReport(
            report_id=secrets.token_urlsafe(24),
            user_id=user_id,
            device_id=device_id,
            score=score,
            findings=findings,
        )

    @staticmethod
    def _finding(
        category: str,
        severity: Severity,
        title: str,
        description: str,
        action: str,
    ) -> DeviceFinding:

        return DeviceFinding(
            finding_id=secrets.token_urlsafe(16),
            category=category,
            severity=severity,
            title=title,
            description=description,
            recommended_action=action,
            requires_user_confirmation=True,
        )

    def calculate_score(
        self,
        findings: list[DeviceFinding]
    ) -> int:

        score = 100

        for finding in findings:
            score -= self.SEVERITY_PENALTY[
                finding.severity
            ]

        return max(0, min(100, score))


# ============================================================
# SAFE REPAIR PLANNER
# ============================================================

class CyberFoxRepairPlanner:

    SAFE_ACTIONS = {
        "update_os",
        "review_or_remove_confirmed_malicious_app",
        "remove_confirmed_malicious_app",
        "review_and_disable_profile",
        "strengthen_security_configuration",
        "review_network_security",
        "review_app_permissions",
        "clear_confirmed_malicious_browser_data",
    }

    @classmethod
    def create_plan(
        cls,
        report: DeviceSecurityReport,
    ) -> list[RepairAction]:

        actions: list[RepairAction] = []

        for finding in report.findings:

            action = finding.recommended_action

            if action not in cls.SAFE_ACTIONS:
                continue

            actions.append(
                RepairAction(
                    action_id=secrets.token_urlsafe(16),
                    report_id=report.report_id,
                    device_id=report.device_id,
                    action=action,
                    reason=finding.title,
                    status=(
                        RepairStatus.WAITING_FOR_CONFIRMATION
                    ),
                    requires_user_confirmation=True,
                )
            )

        return actions

    @staticmethod
    def approve_action(
        repair: RepairAction,
        user_confirmed: bool,
    ) -> RepairAction:

        if not user_confirmed:
            repair.status = RepairStatus.CANCELLED
            return repair

        repair.status = RepairStatus.APPROVED
        repair.approved_at = time.time()

        return repair

    @staticmethod
    def complete_action(
        repair: RepairAction,
        success: bool,
    ) -> RepairAction:

        if success:
            repair.status = RepairStatus.COMPLETED
            repair.completed_at = time.time()
        else:
            repair.status = RepairStatus.FAILED

        return repair


# ============================================================
# OFFICIAL ACCOUNT RECOVERY
# ============================================================

class CyberFoxAccountRecovery:

    PROVIDERS = {
        "instagram",
        "whatsapp",
        "google",
        "apple",
        "microsoft",
    }

    @classmethod
    def create_plan(
        cls,
        provider: str,
    ) -> dict[str, Any]:

        provider = provider.strip().lower()

        if provider not in cls.PROVIDERS:
            raise ValueError(
                "Unsupported account provider."
            )

        return {
            "provider": provider,
            "method": "official_provider_recovery",
            "cyberfox_receives_password": False,
            "cyberfox_stores_password": False,
            "cyberfox_receives_auth_token": False,
            "steps": [
                "open_official_recovery_flow",
                "verify_account_ownership",
                "reset_password_with_provider",
                "enable_mfa",
                "review_active_sessions",
            ],
        }


# ============================================================
# DEVICE ID HASHING
# ============================================================

def privacy_safe_device_identifier(
    device_identifier: str
) -> str:
    """
    Creates a one-way identifier for internal correlation.

    CyberFox should avoid storing unnecessary hardware identifiers.
    """

    if not device_identifier:
        raise ValueError(
            "device_identifier is required."
        )

    return hashlib.sha256(
        device_identifier.encode("utf-8")
    ).hexdigest()


# ============================================================
# CYBERFOX DEVICE PROTECTION SERVICE
# ============================================================

class CyberFoxDeviceProtection:

    def __init__(self) -> None:

        self.consents: dict[
            str,
            DeviceConsent
        ] = {}

        self.reports: dict[
            str,
            DeviceSecurityReport
        ] = {}

        self.repairs: dict[
            str,
            RepairAction
        ] = {}

        self.scanner = CyberFoxDeviceScanner()

        self.repair_planner = CyberFoxRepairPlanner()

    # --------------------------------------------------------
    # USER CONSENT
    # --------------------------------------------------------

    def request_device_access(
        self,
        user_id: str,
        device_id: str,
        permissions: set[str],
        duration_seconds: int = 3600,
    ) -> DeviceConsent:

        consent = (
            DeviceConsentManager.create_consent(
                user_id=user_id,
                device_id=device_id,
                permissions=permissions,
                duration_seconds=duration_seconds,
            )
        )

        self.consents[consent.consent_id] = consent

        return consent

    def revoke_device_access(
        self,
        consent_id: str,
    ) -> None:

        consent = self.consents.get(consent_id)

        if consent is None:
            raise KeyError("Consent not found.")

        DeviceConsentManager.revoke(consent)

    # --------------------------------------------------------
    # DEVICE SCAN
    # --------------------------------------------------------

    def scan_device(
        self,
        user_id: str,
        device_id: str,
        consent_id: str,
        device_data: dict[str, Any],
    ) -> DeviceSecurityReport:

        consent = self.consents.get(consent_id)

        if consent is None:
            raise KeyError("Consent not found.")

        # Extra privacy protection.
        if PrivacyGuard.contains_forbidden_data(
            device_data
        ):
            raise ValueError(
                "Sensitive credentials or authentication "
                "material must not be sent to CyberFox."
            )

        report = self.scanner.scan(
            user_id=user_id,
            device_id=device_id,
            consent=consent,
            device_data=device_data,
        )

        self.reports[report.report_id] = report

        return report

    # --------------------------------------------------------
    # REPAIR PLAN
    # --------------------------------------------------------

    def create_repair_plan(
        self,
        user_id: str,
        report_id: str,
    ) -> list[RepairAction]:

        report = self.reports.get(report_id)

        if report is None:
            raise KeyError("Security report not found.")

        if report.user_id != user_id:
            raise PermissionError(
                "The report does not belong to this user."
            )

        repairs = (
            self.repair_planner.create_plan(report)
        )

        for repair in repairs:
            self.repairs[repair.action_id] = repair

        return repairs

    # --------------------------------------------------------
    # USER CONFIRMATION
    # --------------------------------------------------------

    def approve_repair(
        self,
        user_id: str,
        action_id: str,
        confirmed: bool,
    ) -> RepairAction:

        repair = self.repairs.get(action_id)

        if repair is None:
            raise KeyError("Repair action not found.")

        report = self.reports.get(
            repair.report_id
        )

        if report is None:
            raise KeyError("Security report not found.")

        if report.user_id != user_id:
            raise PermissionError(
                "This repair does not belong to this user."
            )

        return self.repair_planner.approve_action(
            repair=repair,
            user_confirmed=confirmed,
        )

    # --------------------------------------------------------
    # DEVICE AGENT RESULT
    # --------------------------------------------------------

    def record_repair_result(
        self,
        user_id: str,
        action_id: str,
        success: bool,
    ) -> RepairAction:

        repair = self.repairs.get(action_id)

        if repair is None:
            raise KeyError("Repair action not found.")

        report = self.reports.get(
            repair.report_id
        )

        if report is None:
            raise KeyError("Security report not found.")

        if report.user_id != user_id:
            raise PermissionError(
                "This repair does not belong to this user."
            )

        if repair.status != RepairStatus.APPROVED:
            raise PermissionError(
                "Repair must be approved by the user first."
            )

        return self.repair_planner.complete_action(
            repair=repair,
            success=success,
        )


# ============================================================
# EXAMPLE
# ============================================================

if __name__ == "__main__":

    cyberfox = CyberFoxDeviceProtection()

    consent = cyberfox.request_device_access(
        user_id="user-123",
        device_id="device-456",
        permissions={
            "security_scan",
            "malware_scan",
            "installed_apps",
            "privacy_scan",
            "security_configuration",
            "security_report",
        },
        duration_seconds=3600,
    )

    report = cyberfox.scan_device(
        user_id="user-123",
        device_id="device-456",
        consent_id=consent.consent_id,
        device_data={
            "security_updates_missing": True,
            "confirmed_malicious_app": True,
            "weak_security_configuration": True,

            # These must NEVER be accepted:
            # "password": "...",
            # "authentication_token": "...",
        },
    )

    print("Security Score:", report.score)

    repairs = cyberfox.create_repair_plan(
        user_id="user-123",
        report_id=report.report_id,
    )

    for repair in repairs:

        print(
            repair.action,
            "requires confirmation:",
            repair.requires_user_confirmation,
        )
