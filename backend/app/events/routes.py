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
            print("Client disconnected: invalid token (no username)")
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
def on_join(data):
    username = session.get("username")
    room = data.get("room")

    if not username or not room:
        return

    join_room(room)
    print(f"{username} has entered room: {room}")

    chat = query_db("SELECT id FROM chats WHERE chat_name = ?", (room,), one=True)
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

    emit(
        "chat",
        {"message": f"{username} has entered the room.", "username": "System"},
        to=room,
        skip_sid=request.sid,
    )


@socketio.on("leave")
def on_leave(data):
    username = session.get("username")
    room = data.get("room")
    if username and room:
        leave_room(room)
        emit(
            "chat",
            {"message": f"{username} has left the room.", "username": "System"},
            to=room,
        )
        print(f"{username} has left room: {room}")


@socketio.on("message")
def handle_message(data):
    username = session.get("username")
    room = data.get("room")
    message = data.get("message")

    if not username or not room or not message:
        return

    # Get the sender's user ID
    user = query_db("SELECT id FROM users WHERE username = ?", (username,), one=True)
    # Get the chat's ID
    chat = query_db("SELECT id FROM chats WHERE name = ?", (room,), one=True)

    if user and chat:
        sender_id = user["id"]
        chat_id = chat["id"]

        # Store the new message in the database
        query_db(
            "INSERT INTO messages (chat_id, sender_id, content) VALUES (?, ?, ?)",
            (chat_id, sender_id, message),
        )

        # Emit the message to the correct room
        emit("chat", {"message": message, "username": username}, to=room)


@socketio.on("initiate_private_chat")
def handle_private_chat(data):
    current_username = session.get("username")
    other_username = data.get("username")

    if not current_username or not other_username or current_username == other_username:
        return

    other_user = query_db(
        "SELECT id FROM users WHERE username = ?", (other_username,), one=True
    )
    if not other_user:
        # Optionally emit an error back to the initiator
        emit("error", {"message": "User not found."})
        return

    room_name = "_".join(sorted([current_username, other_username]))
    chat = query_db("SELECT id FROM chats WHERE chat_name = ?", (room_name,), one=True)

    if not chat:
        # Create the private chat and add participants
        # This part of the logic remains the same
        query_db(
            "INSERT INTO chats (chat_name, is_public) VALUES (?, ?)", (room_name, 0)
        )
        chat = query_db(
            "SELECT id FROM chats WHERE chat_name = ?", (room_name,), one=True
        )
        current_user_id = query_db(
            "SELECT id FROM users WHERE username = ?", (current_username,), one=True
        )["id"]

        query_db(
            "INSERT INTO participants (user_id, chat_id) VALUES (?, ?), (?, ?)",
            (current_user_id, chat["id"], other_user["id"], chat["id"]),
        )

    # Only notify the user who initiated the chat.
    # The other user will see it on their next refresh via the GET /chats endpoint.
    emit("private_chat_initiated", {"room": room_name, "with_user": other_username})
