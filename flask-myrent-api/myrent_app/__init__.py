from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    
    from myrent_app.landlords import landlords_bp
    from myrent_app.commands import db_manage_bp 
    from myrent_app.errors import errors_bp
    app.register_blueprint(landlords_bp, url_prefix='/api/v1')
    app.register_blueprint(errors_bp)
    app.register_blueprint(db_manage_bp)
    
    return app


