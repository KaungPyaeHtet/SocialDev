from flask_socketio import emit
from app.extensions import socketio
from ..auths.helpers import jwt_required
from flask import session, jsonify


@socketio.on("connect")
def handle_connect():
    pass


@socketio.on("join")
def on_join(data):
    emit('handle_response', data['data'])

@socketio.on("new_message")
def handle_new_message(message):
    username = session.get("username")
    if username:
        print(f"New message from '{username}': {message}")
        emit("chat", {"message": message, "username": username}, broadcast=True)
