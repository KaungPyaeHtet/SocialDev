from flask import jsonify
from . import chat_bp
from ..auths.helpers import query_db, jwt_required


@chat_bp.route("/chats", methods=["GET"])
@jwt_required
def get_user_chats(username):
    user = query_db("SELECT id FROM users WHERE username = ?", (username,), one=True)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_id = user["id"]
    chats = query_db(
        """
        -- Select all private chats and find the other user's name
        SELECT
            c.id,
            c.chat_name,
            c.is_public,
            other_user.username AS display_name
        FROM participants p
        JOIN chats c ON p.chat_id = c.id
        -- Self-join to find the other participant in the same chat
        JOIN participants p2 ON c.id = p2.chat_id AND p.user_id != p2.user_id
        JOIN users other_user ON p2.user_id = other_user.id
        WHERE p.user_id = ? AND c.is_public = 0

        UNION ALL -- Combine with the public chat

        -- Select the public chat
        SELECT
            id,
            chat_name,
            is_public,
            chat_name AS display_name
        FROM chats
        WHERE is_public = 1;
        """,
        (user_id,),
    )

    return jsonify(chats), 200
