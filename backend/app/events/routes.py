# backend/app/events/routes.py
import jwt
from flask import request
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


@socketio.on("join")
def on_join(data):
    username = users.get(request.sid)
    # The client should send a room identifier, e.g., 'public_chat'
    room = data.get("room")

    if not username or not room:
        return

    # Join the socket.io room
    join_room(room)
    print(f"{username} has entered room: {room}")

    # Fetch the chat ID from the database based on the room name
    chat = query_db("SELECT id FROM chats WHERE name = ?", (room,), one=True)
    if chat:
        chat_id = chat["id"]
        # Fetch previous messages for that chat
        messages = query_db(
            """
            SELECT m.content, u.username
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.chat_id = ?
            ORDER BY m.timestamp ASC
            """,
            (chat_id,),
        )

        # Send chat history only to the user who just joined
        for msg in messages:
            emit(
                "chat",
                {"message": msg["content"], "username": msg["username"]},
                to=request.sid,
            )

    # Announce the new user to everyone else in the room
    emit(
        "chat",
        {"message": f"{username} has entered the room.", "username": username},
        to=room,
        # skip_sid is important to prevent the user from getting their own "joined" message twice
        skip_sid=request.sid,
    )


@socketio.on("leave")
def on_leave(data):
    username = users.get(request.sid)
    room = data.get("room")
    if username and room:
        leave_room(room)
        emit(
            "chat",
            {"message": f"{username} has left the room.", "username": username},
            to=room,
        )
        print(f"{username} has left room: {room}")


@socketio.on("message")
def handle_message(data):
    # username = users.get(request.sid)
    # room = data.get("room")
    # message = data.get("message")

    # if not username or not room or not message:
    #     return


    # # Get the sender's user ID
    # user = query_db("SELECT id FROM users WHERE username = ?", (username,), one=True)
    # # Get the chat's ID
    # chat = query_db("SELECT id FROM chats WHERE name = ?", (room,), one=True)

    # if user and chat:
    #     sender_id = user["id"]
    #     chat_id = chat["id"]

    #     # Store the new message in the database
    #     query_db(
    #         "INSERT INTO messages (chat_id, sender_id, content) VALUES (?, ?, ?)",
    #         (chat_id, sender_id, message),
    #     )

    #     # Emit the message to the correct room
    #     emit("chat", {"message": message, "username": username}, to=room)
    message = data.get('message')
    username = data.get('username')
    emit('chat', {"message": message, "username": username}, broadcast=True)