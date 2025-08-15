import sqlite3

from functools import wraps
from flask import request, jsonify, Blueprint, url_for, g, redirect
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    user_data = request.json
    username, email, password = (
        user_data["username"],
        user_data["email"],
        user_data["password"],
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

    return jsonify(user_data)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return jsonify(data)


@login_required
def logout():
    return None

# REST API, JWT, sqlite3 schema
