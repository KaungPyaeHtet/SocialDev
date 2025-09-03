from flask import Flask
from .extensions import socketio
from .auths.helpers import init_helper
from flask_cors import CORS


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = "secret!"

    # Initialize extensions
    socketio.init_app(app)

    # Initialize helper functions
    init_helper(app)

    # Register blueprints
    from .auths import auth

    # Add url prefex such as /auth/register
    app.register_blueprint(auth, url_prefix="/auth")

    # Register the new main blueprint
    from .events import event

    app.register_blueprint(event)

    return app
