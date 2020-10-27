import pytest
from myrent_app import create_app, db


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app
    app.config['DB_FILE_PATH'].unlink()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)
