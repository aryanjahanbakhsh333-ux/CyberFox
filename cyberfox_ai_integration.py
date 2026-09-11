import os
from dataclasses import asdict
from typing import Optional, Dict, Any

from openai import OpenAI

from cyberfox_core import (
    CyberFox,
    SecurityMode,
    SecurityAccess,
    DeviceSecurityScanner,
    DeviceRepairPlanner,
    LegalRecovery,
)

from cyberfox_security_brain import (
    CyberFoxSecurityBrain,
    SecurityRequest,
    SecurityDecision,
)


class CyberFoxAIIntegration:
    """
    اتصال مرکزی CyberFox:

    User
      ↓
    CyberFox Core
      ↓
    Security Access
      ↓
    Security Brain
      ↓
    OpenAI
      ↓
    Security Decision / Recommendation
    """

    def __init__(
        self,
        cyberfox: CyberFox,
        model: Optional[str] = None,
    ):
        self.cyberfox = cyberfox

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv(
            "CYBERFOX_AI_MODEL",
            "gpt-5.6-luna",
        )

        self.client = (
            OpenAI(api_key=self.api_key)
            if self.api_key
            else None
        )

        self.brain = CyberFoxSecurityBrain()
        self.scanner = DeviceSecurityScanner()
        self.repair_planner = DeviceRepairPlanner()
        self.recovery = LegalRecovery()

    # ---------------------------------------------------------
    # AI SYSTEM INSTRUCTIONS
    # ---------------------------------------------------------

    def _system_instructions(
        self,
        is_owner: bool,
        mode: SecurityMode,
    ) -> str:

        if is_owner:
            access_description = """
The authenticated user is the CyberFox owner.

The owner may use:
- White Hat security
- authorized Grey Hat research
- authorized Red Team testing

Grey Hat and Red Team operations are permitted ONLY against:
- assets owned by the owner
- explicitly authorized systems
- controlled laboratory environments

Never perform or provide:
- credential theft
- account takeover
- authentication bypass
- session/token theft
- destructive malware
- ransomware
- persistence malware
- unauthorized access
- real-person phishing
- data exfiltration
- evasion of security controls
"""
        else:
            access_description = """
The authenticated user is a normal CyberFox user.

The user has White Hat defensive access only.

The user may:
- scan their own devices
- improve security
- analyze suspicious links/files
- receive defensive recommendations
- use official account recovery
- receive security education

Grey Hat and Red Team operations are NOT available.
"""

        return f"""
You are CyberFox Security AI.

You are an expert defensive cybersecurity assistant.

Current security mode:
{mode.value}

{access_description}

Core principles:

1. Protect the user and authorized systems.
2. Never request or store passwords.
3. Never request authentication tokens.
4. Never request private keys.
5. Never request recovery codes.
6. Never expose secrets.
7. Prefer least privilege.
8. Prefer temporary authorization.
9. Explain risks clearly.
10. Give practical defensive recommendations.
11. For account recovery, use official provider recovery flows.
12. For device repair, require explicit user confirmation.
13. Never claim an action was executed unless CyberFox actually executed it.
14. Never treat browser-provided authorization flags as trusted.
15. Backend authorization is authoritative.
16. Grey Hat and Red Team actions require trusted backend authorization.
17. If an operation is unsafe or unauthorized, refuse it and provide a safe defensive alternative.

Your job is to analyze security problems, explain them clearly,
produce defensive recommendations, security reports,
threat assessments, remediation plans and security education.
"""

    # ---------------------------------------------------------
    # AUTHORIZATION
    # ---------------------------------------------------------

    def authorize(
        self,
        user_id: str,
        message: str,
        mode: SecurityMode = SecurityMode.WHITE_HAT,
        authorized_asset: bool = False,
        asset_id: Optional[str] = None,
        laboratory_environment: bool = False,
    ) -> SecurityDecision:

        user = self.cyberfox.users.get(user_id)

        if not user:
            raise PermissionError("User not found.")

        is_owner = self.cyberfox.owner_registry.is_owner(
            user_id=user.id,
            email=user.email,
        )

        request = SecurityRequest(
            message=message,
            mode=mode,
            user_id=user_id,
            is_owner=is_owner,
            authorized_asset=authorized_asset,
            asset_id=asset_id,
            laboratory_environment=laboratory_environment,
        )

        return self.brain.analyze_request(request)

    # ---------------------------------------------------------
    # REAL AI CHAT
    # ---------------------------------------------------------

    def chat(
        self,
        user_id: str,
        message: str,
        mode: SecurityMode = SecurityMode.WHITE_HAT,
        authorized_asset: bool = False,
        asset_id: Optional[str] = None,
        laboratory_environment: bool = False,
    ) -> Dict[str, Any]:

        decision = self.authorize(
            user_id=user_id,
            message=message,
            mode=mode,
            authorized_asset=authorized_asset,
            asset_id=asset_id,
            laboratory_environment=laboratory_environment,
        )

        if decision.decision.value == "block":
            return {
                "ok": False,
                "blocked": True,
                "risk": decision.risk.value,
                "reason": decision.reason,
                "safe_alternative": decision.safe_alternative,
            }

        if not self.client:
            return {
                "ok": False,
                "error": "OPENAI_API_KEY is not configured.",
            }

        user = self.cyberfox.users.get(user_id)

        is_owner = bool(
            user
            and self.cyberfox.owner_registry.is_owner(
                user_id=user.id,
                email=user.email,
            )
        )

        instructions = self._system_instructions(
            is_owner=is_owner,
            mode=mode,
        )

        context = {
            "user_id": user_id,
            "owner": is_owner,
            "mode": mode.value,
            "authorized_asset": authorized_asset,
            "asset_id": asset_id,
            "laboratory_environment": laboratory_environment,
            "security_decision": asdict(decision),
        }

        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "CyberFox security context:\n"
                                f"{context}\n\n"
                                "User request:\n"
                                f"{message}"
                            ),
                        }
                    ],
                }
            ],
        )

        return {
            "ok": True,
            "blocked": False,
            "model": self.model,
            "risk": decision.risk.value,
            "decision": decision.decision.value,
            "response": response.output_text,
        }

    # ---------------------------------------------------------
    # SECURITY SCAN + AI ANALYSIS
    # ---------------------------------------------------------

    def analyze_device(
        self,
        user_id: str,
        device_id: str,
        device_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        consent = self.cyberfox.consents.get(
            device_id
        )

        if not consent:
            return {
                "ok": False,
                "error": "Device consent not found.",
            }

        if consent.user_id != user_id:
            return {
                "ok": False,
                "error": "Device does not belong to this user.",
            }

        if not consent.is_valid():
            return {
                "ok": False,
                "error": "Device authorization expired or revoked.",
            }

        scan = self.scanner.scan(device_data)

        if not self.client:
            return {
                "ok": True,
                "scan": scan,
                "ai_analysis": None,
                "message": "OPENAI_API_KEY is not configured.",
            }

        prompt = f"""
Analyze this CyberFox defensive device-security scan.

Scan:
{scan}

Device data:
{device_data}

Return:

1. Overall risk
2. Most important findings
3. Why each finding matters
4. Recommended defensive actions
5. Priority order
6. What the user should NOT do
7. Whether manual confirmation is required

Do not request passwords, tokens, recovery codes,
private keys or other secrets.
"""

        response = self.client.responses.create(
            model=self.model,
            instructions=self._system_instructions(
                is_owner=False,
                mode=SecurityMode.WHITE_HAT,
            ),
            input=prompt,
        )

        return {
            "ok": True,
            "scan": scan,
            "ai_analysis": response.output_text,
        }

    # ---------------------------------------------------------
    # REPAIR PLAN
    # ---------------------------------------------------------

    def create_repair_plan(
        self,
        user_id: str,
        findings: list,
    ) -> Dict[str, Any]:

        plan = self.repair_planner.create_plan(
            findings=findings,
            require_confirmation=True,
        )

        return {
            "ok": True,
            "user_id": user_id,
            "confirmation_required": True,
            "plan": plan,
        }

    # ---------------------------------------------------------
    # OFFICIAL ACCOUNT RECOVERY
    # ---------------------------------------------------------

    def recovery(
        self,
        user_id: str,
        provider: str,
    ) -> Dict[str, Any]:

        allowed = {
            "instagram",
            "whatsapp",
            "google",
            "apple",
            "microsoft",
        }

        provider = provider.lower().strip()

        if provider not in allowed:
            return {
                "ok": False,
                "error": "Unsupported recovery provider.",
            }

        return {
            "ok": True,
            "provider": provider,
            "user_id": user_id,
            "method": "official_provider_recovery",
            "credentials_required": False,
            "message": (
                "CyberFox will guide the user through "
                "the provider's official recovery process."
            ),
        }

    # ---------------------------------------------------------
    # SECURITY REPORT
    # ---------------------------------------------------------

    def security_report(
        self,
        user_id: str,
        message: str,
        mode: SecurityMode = SecurityMode.WHITE_HAT,
        authorized_asset: bool = False,
        asset_id: Optional[str] = None,
        laboratory_environment: bool = False,
    ) -> Dict[str, Any]:

        decision = self.authorize(
            user_id=user_id,
            message=message,
            mode=mode,
            authorized_asset=authorized_asset,
            asset_id=asset_id,
            laboratory_environment=laboratory_environment,
        )

        if decision.decision.value == "block":
            return {
                "ok": False,
                "report": {
                    "risk": decision.risk.value,
                    "decision": decision.decision.value,
                    "reason": decision.reason,
                    "safe_alternative": decision.safe_alternative,
                },
            }

        result = self.chat(
            user_id=user_id,
            message=message,
            mode=mode,
            authorized_asset=authorized_asset,
            asset_id=asset_id,
            laboratory_environment=laboratory_environment,
        )

        return {
            "ok": result.get("ok", False),
            "report": {
                "risk": result.get("risk"),
                "decision": result.get("decision"),
                "analysis": result.get("response"),
            },
        }


# =============================================================
# SINGLE CYBERFOX AI INSTANCE
# =============================================================

cyberfox_ai: Optional[CyberFoxAIIntegration] = None


def connect_cyberfox_ai(
    cyberfox: CyberFox,
) -> CyberFoxAIIntegration:

    global cyberfox_ai

    cyberfox_ai = CyberFoxAIIntegration(
        cyberfox=cyberfox,
        model=os.getenv(
            "CYBERFOX_AI_MODEL",
            "gpt-5.6-luna",
        ),
    )

    return cyberfox_ai


def get_cyberfox_ai() -> CyberFoxAIIntegration:

    if cyberfox_ai is None:
        raise RuntimeError(
            "CyberFox AI has not been connected. "
            "Call connect_cyberfox_ai() during application startup."
        )

    return cyberfox_ai
