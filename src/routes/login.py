from flask import Blueprint
from src.controllers.login import login, protected

login_bp = Blueprint("login", __name__, url_prefix="/login")
login_bp.route("/", methods=["POST"])(login)

auth_bp = Blueprint("protected", __name__, url_prefix="/protected")
auth_bp.route("/", methods=["GET"])(protected)
