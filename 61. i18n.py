SUPPORTED_LANGUAGES = {
    "en": "English",
    "fa": "فارسی",
    "he": "עברית"
}


TRANSLATIONS = {
    "en": {
        "welcome": "Welcome",
        "security_center": "Security Center",
        "dashboard": "Dashboard",
        "free": "Free",
        "pro": "Pro",
        "security_score": "Security Score",
        "threats": "Threats",
        "notifications": "Notifications",
        "emergency_mode": "Emergency Mode",
        "login_required": "Authentication required.",
        "invalid_language": "Unsupported language.",
        "security_ready": "Security system is ready.",
        "threat_detected": "Threat detected.",
        "no_threats": "No threats detected.",
        "pro_required": "Pro plan required.",
        "server_not_authorized": "Server is not authorized."
    },

    "fa": {
        "welcome": "خوش آمدید",
        "security_center": "مرکز امنیت",
        "dashboard": "داشبورد",
        "free": "رایگان",
        "pro": "پرو",
        "security_score": "امتیاز امنیت",
        "threats": "تهدیدها",
        "notifications": "اعلان‌ها",
        "emergency_mode": "حالت اضطراری",
        "login_required": "احراز هویت لازم است.",
        "invalid_language": "زبان پشتیبانی نمی‌شود.",
        "security_ready": "سیستم امنیتی آماده است.",
        "threat_detected": "تهدید شناسایی شد.",
        "no_threats": "تهدیدی شناسایی نشد.",
        "pro_required": "نیاز به پلن Pro دارید.",
        "server_not_authorized": "این سرور مجاز نیست."
    },

    "he": {
        "welcome": "ברוכים הבאים",
        "security_center": "מרכז האבטחה",
        "dashboard": "לוח הבקרה",
        "free": "חינם",
        "pro": "Pro",
        "security_score": "ציון אבטחה",
        "threats": "איומים",
        "notifications": "התראות",
        "emergency_mode": "מצב חירום",
        "login_required": "נדרש אימות.",
        "invalid_language": "השפה אינה נתמכת.",
        "security_ready": "מערכת האבטחה מוכנה.",
        "threat_detected": "זוהה איום.",
        "no_threats": "לא זוהו איומים.",
        "pro_required": "נדרשת תוכנית Pro.",
        "server_not_authorized": "השרת אינו מורשה."
    }
}


def normalize_language(language):
    if not isinstance(language, str):
        return "en"

    language = language.lower().strip()

    if language in SUPPORTED_LANGUAGES:
        return language

    return "en"


def translate(key, language="en"):
    language = normalize_language(language)

    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["en"]
    ).get(
        key,
        TRANSLATIONS["en"].get(key, key)
    )


def get_translations(language="en"):
    language = normalize_language(language)

    return {
        "language": language,
        "name": SUPPORTED_LANGUAGES[language],
        "translations": TRANSLATIONS[language]
    }
