import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return json.dumps({'name': 'Kaung Pyae Htet',
                       'email': 'alice@outlook.com'})

app.run()