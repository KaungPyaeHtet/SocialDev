# backend/app/events/routes.py
import jwt
from app.extensions import socketio
from ..auths.helpers import query_db
from flask import request, session
from flask_socketio import emit, disconnect, join_room, leave_room

key = "secret"


@socketio.on("connect")
def connect():
    access_token = request.headers.get("Authorization")
    if not access_token:
        print("Client disconnected: no token provided")
        disconnect()
        return

    if " " in access_token:  # if the header contains "Bearer", only take token part
        access_token = access_token.split(" ")[1]

    try:
        decoded_token = jwt.decode(access_token, key, algorithms="HS256")
        username = decoded_token.get("username")

        if not username:
            print("Client disconnected: Token is invalid. (no username)")
            disconnect()
            return

        session["username"] = username
        print(f"Client connected: {session['username']} with sid {request.sid}")

    except jwt.ExpiredSignatureError:
        print("Client disconnected: Token has expired.")
        disconnect()
        return

    except jwt.InvalidSignatureError:
        print("Client disconnected: Token is invalid.")
        disconnect()
        return


@socketio.on("disconnect")
def disconnect():
    username = session.get("username", "Anonymous")
    print(f"Client disconnected: {username} with sid {request.sid}")


@socketio.on("join")
def on_join(data): ...


@socketio.on("leave")
def on_leave(data): ...


@socketio.on("message")
def handle_message(data): ...
