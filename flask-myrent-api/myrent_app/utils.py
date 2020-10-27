import jwt
from functools import wraps
from flask import request, abort, current_app
from werkzeug.exceptions import UnsupportedMediaType
# from myrent_app import app


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType('Content type must be application/json')
        return func(*args, **kwargs)
    return wrapper


def token_landlord_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')
        
        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description='Missing token. Please login or register.')

        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])

        if payload['model'] != 'landlords':
            abort(401, description='Missing token. Please login or register.')

        return func(payload['identifier'], *args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')

        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description='Missing token. Please login or register.')

        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])

        return func(payload['identifier'], *args, **kwargs)
    return wrapper
