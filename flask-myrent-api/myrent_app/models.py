import re
import jwt
from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
from werkzeug.datastructures import ImmutableDict
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate
from werkzeug.security import generate_password_hash, check_password_hash
from myrent_app import db


COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(gte|lte|gt|lt)\]')


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Landlord(TimestampMixin, db.Model):
    __tablename__ = 'landlords'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Landlord>: {self.first_name} {self.last_name}'

    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)


    @staticmethod
    def get_schema_args(fields: str) -> dict:
        schema_args = {'many': True}
        if fields:
            schema_args['only'] = [field for field in fields.split(',') if field in Landlord.__table__.columns]
        return schema_args

    @staticmethod
    def apply_order(query: BaseQuery, sort_keys: str) -> BaseQuery:        
        if sort_keys:
            for key in sort_keys.split(','):
                desc = False
                if key.startswith('-'):
                    key = key[1:]
                    desc = True
                column_attr = getattr(Landlord, key, None)
                if column_attr is not None:
                    query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)   
        return query


    @staticmethod
    def _get_filter_argument(column_name: InstrumentedAttribute, 
                            value: str, 
                            operator: str) -> BinaryExpression:
        operator_mapping = {
            '==': column_name == value,
            'gte': column_name >= value,
            'gt': column_name > value,
            'lte': column_name <= value,
            'lt': column_name < value,
        }
        return operator_mapping[operator]


    @staticmethod
    def apply_filter(query: BaseQuery, params: ImmutableDict) -> BaseQuery:
        if params:
            for param, value in params.items():
                if param not in ['fields', 'sort']:
                    operator = '=='
                    match = COMPARISON_OPERATORS_RE.match(param)
                    if match is not None:
                        param, operator = match.groups()
                    column_attr = getattr(Landlord, param, None)
                    if column_attr is not None:
                        filter_argument = Landlord._get_filter_argument(column_attr, value, operator)
                        query = query.filter(filter_argument)
        return query


    def generate_jwt(self) -> bytes:
        payload = {
            'identifier': self.identifier,
            'model': 'landlords',
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class LandlordSchema(Schema):
    id = fields.Integer(dump_only=True)
    identifier = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.String(required=True, validate=validate.Length(max=255))
    first_name = fields.String(required=True, validate=validate.Length(max=100))
    last_name = fields.String(required=True, validate=validate.Length(max=100))
    phone = fields.String(required=True, validate=validate.Length(max=50))
    address = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String()
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6, max=255))
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)


class LandlordUpdatePasswordSchema(Schema):
    current_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))


landlord_schema = LandlordSchema()
landlord_update_password_schema = LandlordUpdatePasswordSchema()
