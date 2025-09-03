CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );

CREATE TABLE
    sqlite_sequence (name, seq);

CREATE TABLE
    chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_name TEXT NOT NULL,
        is_public BOOLEAN NOT NULL DEFAULT 1,
        created_at INTEGER NOT NULL DEFAULT (unixepoch ())
    );

CREATE TABLE
    participants (
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, chat_id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (chat_id) REFERENCES chats (id)
    );

CREATE TABLE
    messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp INTEGER NOT NULL DEFAULT (unixepoch ()),
        FOREIGN KEY (chat_id) REFERENCES chats (id),
        FOREIGN KEY (sender_id) REFERENCES users (id)
    );