from flask import Blueprint

commands_bp = Blueprint('db_manage_cmd', __name__, cli_group=None)

from library_app.commands import db_manage_commands
