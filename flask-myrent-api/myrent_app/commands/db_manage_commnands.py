import os, json
from myrent_app import db
from myrent_app.commands import db_manage_bp
from myrent_app.models import Landlord, Flat
from myrent_app.utils import generate_hashed_password


def load_json_data(filename: str) -> list:
    json_path = os.path.join('C:\\python\\CodersLab\\Python-examples\\flask-myrent-api\\samples', filename)
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@db_manage_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to the database"""
    try:
        data_json = load_json_data('landlords.json')
        for item in data_json:
            item['password'] = generate_hashed_password(item['password'])
            landlord = Landlord(**item)
            db.session.add(landlord)

        data_json = load_json_data('flats.json')
        for item in data_json:
            flat = Flat(**item)
            db.session.add(flat)
        
        db.session.commit()
        print('Data has been added to database')
    except Exception as exc:
        print(f'Unexpected error: {exc}')


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute('DELETE FROM flats')
        db.session.execute('ALTER TABLE flats AUTO_INCREMENT=1')
        db.session.execute('DELETE FROM landlords')
        db.session.execute('ALTER TABLE landlords AUTO_INCREMENT=1')
        print('All data has been deleted')      
    except Exception as exc:
        print(f'Unexpected error: {exc}')
