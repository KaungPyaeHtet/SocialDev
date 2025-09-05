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

    if access_token == "null":
        print("Client disconnected: Invalid token format.")
        disconnect()
        return

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
def on_join():
    messages = query_db("""SELECT * FROM messages ORDER BY timestamp ASC""")
    history = [
        {"username": m["sender_name"], "message": m["content"]} for m in messages
    ]
    emit("chat_history", history, to=request.sid)


@socketio.on("message")
def handle_message(data):
    query_db(
        """INSERT INTO messages (sender_name, content) VALUES (?, ?)""",
        (data["username"], data["message"]),
    )

    emit(
        "chat",
        {"message": data["message"], "username": data["username"]},
        broadcast=True,
    )
