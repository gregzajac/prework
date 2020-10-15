from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from library_app.errors import errors
