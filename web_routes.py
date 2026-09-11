import os

from flask import (
    Blueprint,
    send_from_directory
)


web_routes = Blueprint(
    "web_routes",
    __name__
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


@web_routes.get("/")
def home():
    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


@web_routes.get("/login")
def login_page():
    return send_from_directory(
        BASE_DIR,
        "login.html"
    )


@web_routes.get("/dashboard")
def dashboard_page():
    return send_from_directory(
        BASE_DIR,
        "dashboard.html"
    )


@web_routes.get("/owner")
def owner_page():
    return send_from_directory(
        BASE_DIR,
        "owner.html"
    )


@web_routes.get("/site.css")
def site_css():
    return send_from_directory(
        BASE_DIR,
        "site.css"
    )


@web_routes.get("/login.js")
def login_js():
    return send_from_directory(
        BASE_DIR,
        "login.js"
    )


@web_routes.get("/dashboard.js")
def dashboard_js():
    return send_from_directory(
        BASE_DIR,
        "dashboard.js"
    )
