from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# results = db.session.execute('show databases')
# for row in results:
#     print(row)

from library_app import authors
from library_app import models
from library_app import db_manage_commands
from library_app import errors

# @app.route('/')
# def index():
#     return 'Flask is working'
