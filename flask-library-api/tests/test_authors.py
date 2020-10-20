import pytest


def test_get_authors_no_records(client):
    response = client.get('/api/v1/authors')
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/authors?page=1'
        }        
    }

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_authors(client, sample_data):
    response = client.get('/api/v1/authors')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 5
    assert len(response_data['data']) == 5
    assert response_data['pagination'] == {
        'total_pages': 2,
        'total_records': 10,
        'current_page': '/api/v1/authors?page=1',
        'next_page': '/api/v1/authors?page=2'
    }


def test_get_authors_with_params(client, sample_data):
    response = client.get('/api/v1/authors?fields=first_name&sort=-id&limit=2&page=2')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 2
    assert len(response_data['data']) == 2
    assert response_data['pagination'] == {
        'total_pages': 5,
        'total_records': 10,
        'current_page': '/api/v1/authors?page=2&fields=first_name&sort=-id&limit=2',
        'next_page': '/api/v1/authors?page=3&fields=first_name&sort=-id&limit=2',
        'previous_page': '/api/v1/authors?page=1&fields=first_name&sort=-id&limit=2'
    }
    assert response_data['data'] == [
        {"first_name": "Alice"},
        {"first_name": "Dan"}
    ]


def test_get_single_author(client, sample_data):
    response = client.get('/api/v1/authors/9')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['first_name'] == 'Andrzej'
    assert response_data['data']['last_name'] == 'Sapkowski'
    assert response_data['data']['birth_date'] == '21-06-1948'
    assert len(response_data['data']['books']) == 1


def test_get_single_author_not_found(client):
    response = client.get('/api/v1/authors/90')
    response_data = response.get_json()

    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_author(client, token, author):
    response = client.post('/api/v1/authors', 
                            json=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    expected_result = {
        "data": {
            **author,
            "books": [],
            "id": 1
        },
        "success": True
    }

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result

    response = client.get('/api/v1/authors/1')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'last_name': 'Z', 'birth_date': '22-11-1977'}, 'first_name'),
        ({'first_name': 'G', 'birth_date': '22-11-1977'}, 'last_name'),
        ({'first_name': 'G', 'last_name': 'Z'}, 'birth_date'),
    ]
)
def test_create_author_missing_field(client, token, data, missing_field):
    response = client.post('/api/v1/authors',
                            json=data,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })

    response_data = response.get_json()
    
    assert response.status_code == 400        
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_create_author_invalid_content_type(client, token, author):
    response = client.post('/api/v1/authors',
                            data=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })

    response_data = response.get_json()
    
    assert response.status_code == 415        
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_author_missing_token(client, author):
    response = client.post('/api/v1/authors',
                            json=author)

    response_data = response.get_json()
    
    assert response.status_code == 401       
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
