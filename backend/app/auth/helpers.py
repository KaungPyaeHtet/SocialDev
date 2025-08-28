import sqlite3
from flask import g

DATABASE = "app/users.db"


def init_helper(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dicts."""
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()  # rv - return value
    cur.close()

    if query.lower().strip().startswith(("insert", "update", "delete")):
        db.commit()

    return (rv[0] if rv else None) if one else rv
