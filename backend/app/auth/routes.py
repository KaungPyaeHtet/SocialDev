# backend/app/auth/routes.py

import jwt
import sqlite3
from . import auth
from functools import wraps
from .helpers import query_db
from operator import itemgetter
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

key = "secret"


@auth.route("/register", methods=["POST"])
def register():
    user_data = request.json

    # Checks if all fields exist
    for field in user_data:
        user_data[field] = user_data[field].strip()
        if not user_data[field] or user_data[field] == "":
            return (
                jsonify(
                    {
                        "msg": f"'{field}' field missing or empty",
                    }
                ),
                400,
            )
        else:
            username, email, password = itemgetter("username", "email", "password")(
                user_data
            )

    try:
        hashed_password = generate_password_hash(password)
        query_db(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (
                username,
                email,
                hashed_password,
            ),
        )
    except sqlite3.IntegrityError:
        return jsonify({"msg": "username already exists"}), 422

    return jsonify({"username": username}), 200


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = request.headers.get("Authorization")
        if user is None:
            return jsonify({"msg": "no access token"}), 401

        access_token = jwt.decode(user, key, algorithms="HS256")
        return f(access_token["username"], *args, **kwargs)

    return decorated_function


@auth.route("/login", methods=["POST"])
def login():
    user_data = request.json

    for field in user_data:
        user_data[field] = user_data[field].strip()
        if not user_data[field] or user_data[field] == "":
            return jsonify({"msg": f"'{field}' is empty."}), 400

        else:
            username, email, password = itemgetter("username", "email", "password")(
                user_data
            )

    try:
        user = query_db(
            "SELECT username, email, password FROM users WHERE username = ? AND email = ?",
            (
                username,
                email,
            ),
        )
    except sqlite3.IntegrityError:
        return jsonify({"msg": "user does not exist"}), 404

    if not (user) or not check_password_hash(user["password"], password):
        return jsonify({"msg": "wrong username or password"}), 404

    access_token = jwt.encode({"username": username}, key, algorithm="HS256")
    return jsonify(access_token=access_token)
