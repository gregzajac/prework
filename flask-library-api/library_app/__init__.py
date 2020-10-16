from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)

    from library_app.commands import db_manage_bp
    from library_app.errors import errors_bp
    from library_app.authors import authors_bp
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(authors_bp, url_prefix='/api/v1')

    return app




# results = db.session.execute('show databases')
# for row in results:
#     print(row)