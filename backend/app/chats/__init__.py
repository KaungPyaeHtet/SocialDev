from flask import Blueprint

chat_bp = Blueprint("chat_bp", __name__)

from . import routes
