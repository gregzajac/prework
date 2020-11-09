import pytest


def test_get_landlord_tenants_no_records_no_token(client):
    response = client.get('/api/v1/tenants')
    response_data = response.get_json()
    expected_result = {
        'success': False,
        'message': 'Missing landlord token. Please login or register as landlord.'
    }

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_get_landlord_tenants_no_records_tenant_registered(client, tenant_token):
    response = client.get('/api/v1/tenants', 
                        headers={
                             'Authorization': f'Bearer {tenant_token}' 
                         })
    response_data = response.get_json()
    expected_result = {
        'success': False,
        'message': 'Only landlord functionality.'
    }

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_get_landlord_tenants_no_records_landlord_registered(client, landlord_token):
    response = client.get('/api/v1/tenants', 
                         headers={
                             'Authorization': f'Bearer {landlord_token}' 
                         })
    response_data = response.get_json()
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0
    }

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_get_landlord_tenants_with_data(client, sample_data):
    response = client.post('api/v1/landlords/login', 
                        json={
                            'identifier': 'landlord3',
                            'password': 'haslo3'
                        })
    token = response.get_json()['token']

    assert token

    response = client.get('/api/v1/tenants', 
                         headers={
                             'Authorization': f'Bearer {token}' 
                         })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 3
    assert response_data['number_of_records'] == 3


def test_get_landlord_tenant(client, sample_data):
    response = client.post('api/v1/landlords/login', 
                        json={
                            'identifier': 'landlord3',
                            'password': 'haslo3'
                        })
    token = response.get_json()['token']

    assert token

    response = client.get('/api/v1/tenants/6', 
                         headers={
                             'Authorization': f'Bearer {token}' 
                         })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['identifier'] == 'tenant6'
    assert response_data['data']['email'] == 'mail6@wp.pl'
    assert response_data['data']['first_name'] == 'Magda'
    assert response_data['data']['last_name'] == 'Kowalewska'
    assert response_data['data']['phone'] == '506-500-400'
    assert response_data['data']['address'] == 'Adres 3, ulica1, 3/5'
    assert response_data['data']['description'] == 'Opis 6'
    assert response_data['data']['landlord'] == {
                                                    'identifier': 'landlord3',
                                                    'first_name': 'Irena',
                                                    'last_name': 'Kowalska'
                                                }


def test_create_tenant_without_token(client):
    tenant = {
        "address": "testaddress",
        "description": "testtenantdescription",
        "email": "testtenantmail@wp.pl",
        "first_name": "testfirst_name",
        "identifier": "testtenant",
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testtenant"
    }    
    response = client.post('/api/v1/tenants', json=tenant)
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    alert = 'Missing landlord token. Please login or register as landlord.'
    assert response_data['message'] == alert


def test_create_tenant_with_tenant_token(client, tenant_token):
    tenant = {
        "address": "testaddress",
        "description": "testtenantdescription",
        "email": "testtenantmail@wp.pl",
        "first_name": "testfirst_name",
        "identifier": "testtenant",
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testtenant"
    }    
    response = client.post('/api/v1/tenants', 
                            json=tenant,
                            headers={
                                'Authorization': f'Bearer {tenant_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    alert = 'Only landlord functionality.'
    assert response_data['message'] == alert


def test_create_tenant_with_landlord_token(client, landlord, landlord_token):
    tenant = {
        "address": "testaddress",
        "description": "testtenantdescription",
        "email": "testtenantmail@wp.pl",
        "first_name": "testfirst_name",
        "identifier": "testtenant",
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testtenant"
    }    
    response = client.post('/api/v1/tenants', 
                            json=tenant,
                            headers={
                                'Authorization': f'Bearer {landlord_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['identifier'] == tenant['identifier']
    assert response_data['data']['description'] == tenant['description']
    assert response_data['data']['email'] == tenant['email']
    assert response_data['data']['first_name'] == tenant['first_name']
    assert response_data['data']['last_name'] == tenant['last_name']
    assert response_data['data']['phone'] == tenant['phone']
    assert response_data['data']['landlord'] == {
                                            'identifier': landlord['identifier'],
                                            'first_name': landlord['first_name'],
                                            'last_name': landlord['last_name']
                                        }


def test_create_tenant_existing_identifier(client, landlord, landlord_token, tenant):
    tenant = {
        "identifier": tenant['identifier'],
        "address": "testaddress",
        "description": "testtenantdescription",
        "email": "testtenantmail@wp.pl",
        "first_name": "testfirst_name",
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testtenant"
    }    
    response = client.post('/api/v1/tenants', 
                            json=tenant,
                            headers={
                                'Authorization': f'Bearer {landlord_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    alert = f'Tenant with identifier {tenant["identifier"]} already exists'
    assert response_data['message'] == alert


def test_create_tenant_existing_email(client, landlord, landlord_token, tenant):
    tenant = {
        "identifier": 'testidentifier',
        "email": tenant['email'],
        "address": "testaddress",
        "description": "testtenantdescription",
        "first_name": "testfirst_name",
        "last_name": "testlast_name",
        "phone": "testphone",
        "password": "testtenant"
    }    
    response = client.post('/api/v1/tenants', 
                            json=tenant,
                            headers={
                                'Authorization': f'Bearer {landlord_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    alert = f'Tenant with email {tenant["email"]} already exists'
    assert response_data['message'] == alert


def test_login_tenant(client, tenant, tenant_token):
    response = client.post('/api/v1/tenants/login',
                            json={
                                'identifier': tenant['identifier'],
                                'password': tenant['password']
                            },
                            headers={
                                'Authorization': f'Bearer {tenant_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert 'token' in response_data


def test_login_tenant_wrong_identifier(client, tenant, tenant_token):
    response = client.post('/api/v1/tenants/login',
                            json={
                                'identifier': 'wrongidentifier',
                                'password': tenant['password']
                            },
                            headers={
                                'Authorization': f'Bearer {tenant_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert response_data['message'] == 'Invalid credentials'


def test_login_tenant_wrong_password(client, tenant, tenant_token):
    response = client.post('/api/v1/tenants/login',
                            json={
                                'identifier': tenant['identifier'],
                                'password': 'wrongpassword'
                            },
                            headers={
                                'Authorization': f'Bearer {tenant_token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert response_data['message'] == 'Invalid credentials'


def test_get_current_tenant_without_token(client, tenant):
    response = client.get('/api/v1/tenants/me')
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login or register.'


def test_get_current_tenant(client, tenant, tenant_token):
    response = client.get('/api/v1/tenants/me',
                        headers={
                            'Authorization': f'Bearer {tenant_token}'
                        })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['identifier'] == tenant['identifier']
    assert response_data['data']['description'] == tenant['description']
    assert response_data['data']['email'] == tenant['email']
    assert response_data['data']['first_name'] == tenant['first_name']
    assert response_data['data']['last_name'] == tenant['last_name']
    assert response_data['data']['phone'] == tenant['phone']
    assert response_data['data']['landlord']


# def test_update_tenant_password_by_landlord(client, landlord, tenant, landlord_token):
#     response = client.put('/api/v1/tenants/password',
#                         json={
#                             'current_password': tenant['password'],
#                             'new_password': 'newtenantpassword'
#                         }
#                         headers={
#                             'Authorization': f'Bearer {landlord_token}'
#                         })
#     response_data = response.get_json()

#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#     assert response_data['success'] is True    