import sqlite3

from functools import wraps
from operator import itemgetter
from flask import request, jsonify, Blueprint, url_for, g, redirect
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    user_data = request.json

    # Checks if all fields exist
    for field in user_data:
        user_data[field] = user_data[field].strip()
        if not user_data[field] or user_data[field] == "":
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"The '{field}' field is required and cannot be empty.",
                    }
                ),
                400,
            )
        else:
            username, email, password = itemgetter("username", "email", "password")(
                user_data
            )

    try:
        with sqlite3.connect("users.db") as conn:
            db = conn.cursor()
            hashed_password = generate_password_hash(password)

            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (
                    username,
                    email,
                    hashed_password,
                ),
            )
            conn.commit()

    except sqlite3.Error:
        return jsonify("Username already exists."), 422

    return jsonify({"status": "success", "username": username})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/login", methods=["POST"])
def login():
    # Return JWT with cookies
    # Make users don't have to sign in frequent.
    user_data = request.json

    for field in user_data:
        user_data[field] = user_data[field].strip()
        if not user_data[field] or user_data[field] == "":
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"The '{field}' field is required and cannot be empty.",
                    }
                ),
                400,
            )
        else:
            username, email, password = itemgetter("username", "email", "password")(
                user_data
            )

    try:
        with sqlite3.connect("users.db") as conn:
            conn.row_factory = sqlite3.Row
            db = conn.cursor()
            user = db.execute(
                "SELECT username, email FROM users WHERE username = ? AND email = ?"(
                    username,
                    email,
                    password,
                )
            ).fetchall
    except sqlite3.Error:
        return jsonify({"message": "account does not exist"}), 500

    if not user or check_password_hash(user["password"], password):
        return jsonify({"message": "fail", "error": "invalid email or password"})


@login_required
def logout(): ...


# REST API, JWT, sqlite3 schema
