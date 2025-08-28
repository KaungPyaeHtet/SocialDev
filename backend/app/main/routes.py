# backend/app/main/routes.py

from . import main
from flask import jsonify


# This is a basic route for the homepage of your application
@main.route("/")
def index():
    """Serves the main homepage."""
    return jsonify({"message": "Welcome to the main page!"})


# You could add other general-purpose routes here
@main.route("/about")
def about():
    """Serves the about page."""
    return jsonify({"about": "This is the about page."})
