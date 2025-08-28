from flask_socketio import emit
from app.extensions import socketio
from ..auths.helpers import jwt_required
from flask import session, jsonify


@socketio.on("connect")
@jwt_required
def handle_connect(username):
    session["username"] = username
    print(f"Client connected: {session['username']}")


@socketio.on("join")
def on_join(data):
    username = session.get("username")
    if username:
        print(f"User '{username}' has joined.")
    else:
        return jsonify({"msg": "unauthorized"}), 401


@socketio.on("new_message")
def handle_new_message(message):
    username = session.get("username")
    if username:
        print(f"New message from '{username}': {message}")
        emit("chat", {"message": message, "username": username}, broadcast=True)
