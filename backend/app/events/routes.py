from flask import session
from flask_socketio import emit
from app.extensions import socketio
from ..auths.helpers import query_db, jwt_required

users = {}


@socketio.on("connect")
@jwt_required
def handle_connect():
    print("Client connected!")
