import pytest


def test_registration(client):
    response = client.post('/api/v1/auth/register',
                            json={
                                'username': 'gz',
                                'password': '1234567',
                                'email': 'newemail@o2.pl'
                            })

    response_data = response.get_json()
    
    assert response.status_code == 201        
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'username': 'gz', 'password': '1234567'}, 'email'),
        ({'username': 'gz', 'email': 'newemail@o2.pl'}, 'password'),
        ({'password': '1234567', 'email': 'newemail@o2.pl'}, 'username'),
    ]
)
def test_registration_invalid_data(client, data, missing_field):
    response = client.post('/api/v1/auth/register',
                            json=data)

    response_data = response.get_json()
    
    assert response.status_code == 400        
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_registration_invalid_content_type(client):
    response = client.post('/api/v1/auth/register',
                            data={
                                'username': 'gz',
                                'password': '1234567',
                                'email': 'newemail@o2.pl'
                            })

    response_data = response.get_json()
    
    assert response.status_code == 415        
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_username(client, user):
    response = client.post('/api/v1/auth/register',
                            json={
                                'username': user['username'],
                                'password': '1234567',
                                'email': 'newemail123@o2.pl'
                            })

    response_data = response.get_json()
    
    assert response.status_code == 409       
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_email(client, user):
    response = client.post('/api/v1/auth/register',
                            json={
                                'username': 'newtestusername',
                                'password': '1234567',
                                'email': user['email']
                            })

    response_data = response.get_json()
    
    assert response.status_code == 409       
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
