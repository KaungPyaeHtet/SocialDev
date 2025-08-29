# backend/app/events/routes.py
import jwt
from flask import request, session
from flask_socketio import emit, disconnect, join_room, leave_room
from app.extensions import socketio
from ..auths.helpers import query_db

key = "secret"
users = {}


@socketio.on("connect")  # Handshake - Authentication stage
def connect():
    access_token = request.headers.get("Authorization")
    if not access_token:
        print("Client disconnected: No token provided.")
        disconnect()
        return

    # Remove "Bearer" prefix in the token if it exists
    if " " in access_token:
        access_token = access_token.split(" ")[1]

    try:
        decoded_token = jwt.decode(access_token, key, algorithms=["HS256"])
        username = decoded_token.get("username")
        if not username:
            print("Client disconnected: Token is invalid (no username).")
            disconnect()
            return

        users[request.sid] = username
        print(f"Client connected: {username} with sid {request.sid}")

    except jwt.ExpiredSignatureError:
        print("Client disconnected: Token has expired.")
        disconnect()
        return

    except jwt.InvalidTokenError:
        print("Client disconnected: Token is invalid.")
        disconnect()
        return


@socketio.on("disconnect")
def disconnect():
    username = users.pop(request.sid, None)
    if username:
        print(f"Client disconnected: {username} with sid {request.sid}")
    else:
        print(f"Anonymous client disconnected: sid {request.sid}")


@socketio.on("join")  # join_room method must be applied here
def on_join(data):
    username = users.get(request.sid)
    if not username:
        print(f"Received event from unknown user with sid {request.sid}")
        return

    chat_id = 1
    join_room(chat_id)
    socketio.send(f"{username} has entered the room {chat_id}")


@socketio.on("leave")  # leave_room method must be applied here
def on_leave(data):
    username = users.get(request.sid)
    if not username:
        print(f"Received event from unknown user with sid {request.sid}")
        return

    chat_id = 1
    leave_room(chat_id)
    socketio.send(f"{username} has leave the room {chat_id}")


@socketio.on("message")
def handle_message(message):
    print(f"New message: {message}")
    username = users.get(request.sid)
    emit("chat", {"message": message, "username": username}, broadcast=True)


# @socketio.on("connect")
# def handle_connect():
#     token = request.headers.get("Authorization")
#     if not token:
#         print("Client disconnected: No token provided.")
#         disconnect()
#         return

#     # Remove "Bearer" prefix, if exists
#     if " " in token:
#         token = token.split(" ")[1]

#     try:
#         decoded_token = jwt.decode(token, key, algorithms=["HS256"])
#         username = decoded_token.get("username")
#         if not username:
#             print("Client disconnected: Token is invalid (no username).")
#             disconnect()
#             return

#         session["username"] = username
#         print(f"Client connected: {username}")

#     except jwt.ExpiredSignatureError:
#         print("Client disconnected: Token has expired.")
#         disconnect()
#         return

#     except jwt.InvalidTokenError:
#         print("Client disconnected: Token is invalid.")
#         disconnect()
#         return


# @socketio.on("disconnect")
# def handle_disconnect():
#     username = session.get("username")
#     print(f"Client disconnected: {username}")


# @socketio.on("join")
# def on_join(data):
#     username = session.get("username")
#     if not username:
#         return

#     print(f"Received 'join' event from {username} with data: {data}")
#     emit("handle_response", {"message": f"Hello, {username}!", "data": data["data"]})
