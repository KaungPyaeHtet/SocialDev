# backend/app/__init__.py

from flask import Flask
from .extensions import socketio
from .auth.helpers import init_helper


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret!"

    # Initialize extensions
    socketio.init_app(app)

    # Initialize helper functions
    init_helper(app)

    # Register blueprints
    from .auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Register the new main blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    return app
