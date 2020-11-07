import jwt
from flask import current_app
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate
from werkzeug.security import check_password_hash
from myrent_app import db


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
    flats = db.relationship('Flat', back_populates='landlord')
    tenants = db.relationship('Tenant', back_populates='landlord')


    def __repr__(self):
        return f'<Landlord>: {self.first_name} {self.last_name}'

    def generate_jwt(self) -> bytes:
        jwt_expired_minutes = current_app.config.get('JWT_EXPIRED_MINUTES', 30)
        payload = {
            'id': self.id,
            'model': 'landlords',
            'exp': datetime.utcnow() + timedelta(minutes=jwt_expired_minutes)
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Flat(TimestampMixin, db.Model):
    __tablename__ = 'flats'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')  #active/inactive/sold
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)
    landlord = db.relationship('Landlord', back_populates='flats')

    def __repr__(self):
        return f'id: {self.id} - {self.identifier}'


class Tenant(TimestampMixin, db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)
    landlord = db.relationship('Landlord', back_populates='tenants')

    def __repr__(self):
        return f'<Tenant>: {self.first_name} {self.last_name}'


class LandlordSchema(Schema):
    id = fields.Integer(dump_only=True)
    identifier = fields.String(required=True, validate=validate.Length(min=3, max=255))
    email = fields.String(required=True, validate=validate.Length(max=255))
    first_name = fields.String(required=True, validate=validate.Length(max=100))
    last_name = fields.String(required=True, validate=validate.Length(max=100))
    phone = fields.String(required=True, validate=validate.Length(max=50))
    address = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String()
    password = fields.String(load_only=True, required=True, 
                    validate=validate.Length(min=6, max=255))
    flats = fields.List(fields.Nested(lambda: FlatSchema(exclude=['landlord'])))
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)


class LandlordUpdatePasswordSchema(Schema):
    current_password = fields.String(required=True, load_only=True, 
                            validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, 
                        validate=validate.Length(min=6, max=255))


class FlatSchema(Schema):
    id = fields.Integer(dump_only=True)
    identifier = fields.String(required=True, 
                    validate=validate.Length(min=3, max=255))
    address = fields.String(required=True, 
                    validate=validate.Length(min=3, max=255))
    description = fields.String()
    status = fields.String()
    landlord_id = fields.Integer(load_only=True)
    landlord = fields.Nested(lambda: LandlordSchema(only=['identifier', 
                                                         'first_name', 
                                                         'last_name']))
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)


class TenantSchema(Schema):
    id = fields.Integer(dump_only=True)
    identifier = fields.String(required=True, validate=validate.Length(min=3, max=255))
    email = fields.String(required=True, validate=validate.Length(max=255))
    first_name = fields.String(required=True, validate=validate.Length(max=100))
    last_name = fields.String(required=True, validate=validate.Length(max=100))
    phone = fields.String(required=True, validate=validate.Length(max=50))
    address = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String()
    password = fields.String(load_only=True, required=True, 
                    validate=validate.Length(min=6, max=255))
    landlord_id = fields.Integer(load_only=True)
    landlord = fields.Nested(lambda: LandlordSchema(only=['identifier', 
                                                         'first_name', 
                                                         'last_name']))
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)    


landlord_schema = LandlordSchema()
landlord_update_password_schema = LandlordUpdatePasswordSchema()
flat_schema = FlatSchema()
tenant_schema = TenantSchema()
