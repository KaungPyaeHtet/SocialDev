import jwt
import sqlite3
from flask import g
from functools import wraps
from flask import request, jsonify
from email_validator import validate_email, EmailNotValidError

DATABASE = "app/users.db"
key = "secret"


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = request.headers.get("Authorization")
        if user is None:
            return jsonify({"msg": "no access token"}), 401

        access_token = jwt.decode(user, key, algorithms="HS256")
        return f(access_token["username"], *args, **kwargs)

    return decorated_function


def init_helper(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)


def check_email(email) -> bool:
    try:
        # validate and get info
        v = validate_email(email)
        # replace with normalized form
        email = v["email"]
        return True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return False


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dicts."""
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()  # rv - return value
    cur.close()

    if query.lower().strip().startswith(("insert", "update", "delete")):
        db.commit()

    return (rv[0] if rv else None) if one else rv
