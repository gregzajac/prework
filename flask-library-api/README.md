# Library REST API

REST API for online library. It supports authors of books and books resources including authentication (JWT)

The documentation can be found in 'documentation.html' or [here](https://documenter.getpostman.com/view/13065363/TVYCAfLU)

## Setup

- Clone repository
- Create database and user
- Rename .env.example to '.env' and set your values 
    (for MySQL SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4')
- Create a virtual environment (python -m venv venv)
- Install packages from requirements.txt (pip install -r requirements.txt)
- Migrate database (flask db upgrade)
- Run command (flask run)

### NOTE

Import / delete example data from library_app/samples

import: flask db-manage add-data
remove: flask db-manage remove-data

## Tests

In order to execute test located in /tests run: python -m pytest /tests

## Technologies / Tools

- Python 3.7.3
- Flask 1.1.2
- Alembic 1.4.3
- SQL Alchemy 1.3.20
- Pytest 6.1.1
- MySQL
- AWS
- Postman

