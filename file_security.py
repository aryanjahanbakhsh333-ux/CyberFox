import hashlib


MAX_FILE_SIZE = 10 * 1024 * 1024


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".docx",
    ".xlsx",
    ".zip"
}


def sha256_bytes(data):

    return hashlib.sha256(
        data
    ).hexdigest()


def analyze_file(
    filename,
    data
):

    if not filename:
        return {
            "success": False,
            "error": "Filename is required."
        }

    if not isinstance(
        data,
        bytes
    ):
        return {
            "success": False,
            "error": "File data must be bytes."
        }

    if len(data) > MAX_FILE_SIZE:
        return {
            "success": False,
            "error": "File is too large."
        }

    lower_name = filename.lower()

    extension = ""

    if "." in lower_name:
        extension = "." + lower_name.rsplit(
            ".",
            1
        )[1]

    if extension not in ALLOWED_EXTENSIONS:
        return {
            "success": False,
            "error": "File type is not supported."
        }

    return {
        "success": True,
        "filename": filename,
        "size": len(data),
        "sha256": sha256_bytes(data),
        "status": "ready_for_reputation_scan"
    }
