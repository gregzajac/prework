import os
from pathlib import Path
from dotenv import load_dotenv


base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRED_MINUTES = 30
    PER_PAGE = 5
    CORS_HEADERS = 'Content-Type'
    VERSION = 'v1'
    UPLOAD_FOLDER = ''


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = base_dir / 'static' / 'pictures'


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}