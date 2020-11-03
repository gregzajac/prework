import pytest
from myrent_app import create_app, db
from myrent_app.commands.db_manage_commnands import add_data


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
def landlord(client):
    landlord = {
        "address": "testaddress", 
        "description": "testdescription", 
        "email": "testmail@wp.pl", 
        "first_name": "testfirst_name", 
        "identifier": "testidentifier", 
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testpassword"
    }

    client.post('/api/v1/landlords/register', 
                json=landlord)
    return landlord


@pytest.fixture
def landlord_token(client, landlord):
    response = client.post('/api/v1/landlords/login', 
                            json={
                                'identifier': landlord['identifier'],
                                'password': landlord['password']
                            })
    response_data = response.get_json()
    return response_data['token']
  

@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)


@pytest.fixture
def flat():
    return {
        'identifier': 'testidentifier',
        'address': 'testaddress',
        'description': 'testdescription'
    }

@pytest.fixture
def flat_2():
    return {
        'identifier': 'testidentifier2',
        'address': 'testaddress2',
        'description': 'testdescription2'
    }