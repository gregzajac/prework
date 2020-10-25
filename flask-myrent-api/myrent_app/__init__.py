from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# result = db.session.execute('show databases;')
# for row in result:
#     print(row)

from myrent_app import landlords
from myrent_app import models
from myrent_app import db_manage_commnands
