from functools import wraps
from flask import request, jsonify, Blueprint, url_for, g, redirect
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("login", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect("login", next=request.url)
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return jsonify(data)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return jsonify(data)


# @login_required
# def logout():

# REST API, JWT, sqlite3 schema
