import pytest


def test_get_all_flats_no_records(client):
    response = client.get('/api/v1/flats')
    response_data = response.get_json()
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/flats?page=1'
        }
    }    
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data == expected_result


def test_get_all_flats(client, sample_data):
    response = client.get('/api/v1/flats')
    response_data = response.get_json()   
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination'] == {
            'total_pages': 2,
            'total_records': 6,
            'current_page': '/api/v1/flats?page=1',
            'next_page': '/api/v1/flats?page=2'
        }


def test_get_all_flats_with_params(client, sample_data):
    response = client.get('/api/v1/flats?fields=id,identifier&sort=-id&id[gte]=2&limit=2&page=2')
    response_data = response.get_json()
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 2
    # assert response_data['pagination'] == {
    #         "current_page": "/api/v1/flats?page=2&fields=id,identifier&sort=-id&id[gte]=2&limit=2", 
    #         "next_page": "/api/v1/flats?page=3&fields=id,identifier&sort=-id&id[gte]=2&limit=2", 
    #         "previous_page": "/api/v1/flats?page=1&fields=id,identifier&sort=-id&id[gte]=2&limit=2", 
    #         "total_pages": 3, 
    #         "total_records": 5
    #     }
    assert response_data['data'] == [
            {
            "id": 4, 
            "identifier": "Chopina 5"
            }, 
            {
            "id": 3, 
            "identifier": "Tołstoja 3"
            }
        ]


def test_get_one_flat(client, sample_data):
    response = client.get('/api/v1/flats/1')
    response_data = response.get_json()
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['identifier'] == 'Mostnika 5'
    assert response_data['data']['address'] == 'Mostnika 5/12 01-100 Słupsk'
    assert response_data['data']['description'] == 'Mieszkanie dwupokojowe z aneksem kuchennym na trzecim piętrze.'
    assert response_data['data']['landlord']['identifier'] == '01'
    assert response_data['data']['landlord']['first_name'] == 'Jan'
    assert response_data['data']['landlord']['last_name'] == 'Kowalski'


def test_get_all_landlord_flats(client, sample_data):
    response = client.get('/api/v1/landlords/2/flats')
    response_data = response.get_json()
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True  
    assert response_data['number_of_records'] == 2
    assert len(response_data['data']) == 2


def test_create_flat(client, landlord, flat, landlord_token):
    response = client.post('/api/v1/flats', 
                        json=flat,
                        headers={
                            'Authorization': f'Bearer {landlord_token}'
                        })
    response_data = response.get_json()

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['identifier'] == flat['identifier']
    assert response_data['data']['address'] == flat['address']
    assert response_data['data']['status'] == 'active'
    assert response_data['data']['landlord']['identifier'] == landlord['identifier']
    assert response_data['data']['landlord']['first_name'] == landlord['first_name']
    assert response_data['data']['landlord']['last_name'] == landlord['last_name']


