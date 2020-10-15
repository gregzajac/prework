import json, os
from pathlib import Path
from datetime import datetime

from library_app import db
from library_app.models import Author

from library_app.commands import commands_bp


@commands_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to the database"""
    try:
        authors_path = os.path.abspath('C:\python\CodersLab\Python-examples\flask-library-api\samples\authors.json')
        # authors_path = os.path.join(os.getcwd(), 'samples', 'authors.json')
        # authors_path = Path(__file__).parent.parent / 'samples' / 'authors.json'
        with open(authors_path) as file:
            data_json = json.load(file)

        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)
        db.session.commit()
        print('Data has been added to database')

    except Exception as exc:
        print(f'Unexpected error: {exc}')


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute('TRUNCATE TABLE authors')
        db.session.commit()
        print('Data has been removed from database')
    except Exception as exc:
        print(f'Unexpected error: {exc}')
