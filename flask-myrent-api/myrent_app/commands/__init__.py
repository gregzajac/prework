from flask import Blueprint

db_manage_bp = Blueprint('db_manage_cmd', __name__)

from myrent_app.commands import db_manage_bp
