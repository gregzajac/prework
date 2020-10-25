from datetime import datetime
from myrent_app import db


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Landlord(TimestampMixin, db.Model):
    __tablename__ = 'landlords'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Landlord>: {self.first_name} {self.last_name}'
