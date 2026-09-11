from url_security import analyze_url
from phishing_detector import detect_phishing
from file_security import analyze_file


def scan_url(url):

    result = analyze_url(
        url
    )

    return {
        "type": "url",
        "result": result
    }


def scan_message(text):

    result = detect_phishing(
        text
    )

    return {
        "type": "message",
        "result": result
    }


def scan_file(
    filename,
    data
):

    result = analyze_file(
        filename,
        data
    )

    return {
        "type": "file",
        "result": result
    }
