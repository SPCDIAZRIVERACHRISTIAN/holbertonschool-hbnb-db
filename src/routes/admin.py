'''This module contains the routes for admin data.'''

from flask import Blueprint
from src.controllers.admin import admin_data


admin_bp = Blueprint("admin", __name__, url_prefix="/admin/data")

admin_bp.route("/", methods=["POST", 'DELETE'])(admin_data)
