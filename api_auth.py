from flask import Blueprint, request, jsonify

from auth_service import create_user, authenticate_user
from session_service import create_session, delete_session, get_session


auth_api = Blueprint(
    "auth_api",
    __name__,
    url_prefix="/api/auth"
)


@auth_api.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "error": "Email and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "error": "Password must be at least 8 characters."
        }), 400

    user, error = create_user(
        email,
        password
    )

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 409

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "user_id": user.id
    }), 201


@auth_api.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "")
    password = data.get("password", "")

    user = authenticate_user(
        email,
        password
    )

    if not user:
        return jsonify({
            "success": False,
            "error": "Invalid email or password."
        }), 401

    token = create_session(user.id)

    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "plan": user.plan,
            "role": user.role
        }
    })


@auth_api.post("/logout")
def logout():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        delete_session(token)

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


@auth_api.get("/me")
def current_user():
    authorization = request.headers.get(
        "Authorization",
        ""
    )

    if not authorization.startswith("Bearer "):
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    token = authorization[7:].strip()
    session = get_session(token)

    if not session:
        return jsonify({
            "success": False,
            "error": "Invalid or expired session."
        }), 401

    return jsonify({
        "success": True,
        "user_id": session["user_id"]
    })
