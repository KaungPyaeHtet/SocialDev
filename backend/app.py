import jwt

from routes.auth import auth_bp, jwt_required
from flask import Flask, jsonify, request, make_response, session
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(auth_bp)
CORS(app)

key = "secret"


@app.route("/")
def index():
    return jsonify({"name": "Kaung Pyae Htet", "email": "alice@outlook.com"})


@app.route("/users/<user>")
@jwt_required
def show_user_profile(username, user):
    return jsonify(username)


if __name__ == "__main__":
    app.run(debug=True)
