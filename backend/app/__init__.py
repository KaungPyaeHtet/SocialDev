from flask import Flask
from .extensions import socketio
from .auths.helpers import init_helper

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret!"

    # Initialize extensions
    socketio.init_app(app)

    # Initialize helper functions
    init_helper(app)

    # Register blueprints
    from .auths import auth

    app.register_blueprint(auth, url_prefix="/auth")

    # Register the new main blueprint
    from .events import event

    app.register_blueprint(event)

    return app
