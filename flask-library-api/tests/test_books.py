import pytest


def test_get_books_no_data(client):
    response = client.get('/api/v1/books')
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/books?page=1'
        }
    }

    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_get_books(client, sample_data):
    response = client.get('/api/v1/books')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination']['total_pages'] == 3
    assert response_data['pagination']['current_page'] == '/api/v1/books?page=1'
    assert response_data['pagination']['next_page'] == '/api/v1/books?page=2'


def test_get_books_with_params(client, sample_data):
    response = client.get('/api/v1/books?id[lte]=5&sort=-id&fields=id,title&page=2&limit=2')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 2
    assert response_data['number_of_records'] == 2
    assert response_data['pagination'] == {
        'total_pages': 3,
        'total_records': 5,
        'current_page': "/api/v1/books?page=2&id%5Blte%5D=5&sort=-id&fields=id%2Ctitle&limit=2",
        'next_page': "/api/v1/books?page=3&id%5Blte%5D=5&sort=-id&fields=id%2Ctitle&limit=2",
        'previous_page': "/api/v1/books?page=1&id%5Blte%5D=5&sort=-id&fields=id%2Ctitle&limit=2"
    }


def test_get_book(client, sample_data):
    response = client.get('/api/v1/books/1')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['id'] == 1
    assert response_data['data']['isbn'] == 9780141036137
    assert response_data['data']['number_of_pages'] == 112
    assert response_data['data']['title'] == 'Animal Farm'
    assert response_data['data']['author'] == {
        'id': 1,
        'first_name': 'George',
        'last_name': 'Orwell'
    }


def test_get_book_not_found(client, sample_data):
    response = client.get('/api/v1/books/100')
    response_data = response.get_json()

    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_book(client, token, book, author):
    response = client.post('/api/v1/authors', 
                            json=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response = client.get('/api/v1/authors/1')
    response_data = response.get_json()

    assert response_data['data']['id'] == 1

    response = client.post('/api/v1/authors/1/books', 
                            json=book,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    
    expected_result = {
        'data': {
            'author': {
                'id': 1,
                'first_name': author['first_name'],
                'last_name': author['last_name']
            },
            **book,
            'id': 1
        },
        'success': True
    }

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result

    response = client.get('/api/v1/books/1')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_create_book_invalid_content_type(client, token, author, book):
    response = client.post('/api/v1/authors', 
                            json=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response = client.get('/api/v1/authors/1')
    response_data = response.get_json()

    assert response_data['data']['id'] == 1

    response = client.post('/api/v1/authors/1/books', 
                            data=book,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()

    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_book_missing_token(client, token, author, book):
    response = client.post('/api/v1/authors', 
                            json=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response = client.get('/api/v1/authors/1')
    response_data = response.get_json()

    assert response_data['data']['id'] == 1

    response = client.post('/api/v1/authors/1/books', 
                            json=book)
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'title': 'testbook', 'isbn': 1212121212121}, 'number_of_pages'),
        ({'title': 'testbook', 'number_of_pages': 100}, 'isbn'),
        ({'number_of_pages': 100, 'isbn': 1212121212121}, 'title')
    ]
)
def test_create_book_missing_field(client, token, author, data, missing_field):
    response = client.post('/api/v1/authors', 
                            json=author,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response = client.get('/api/v1/authors/1')
    response_data = response.get_json()

    assert response_data['data']['id'] == 1

    response = client.post('/api/v1/authors/1/books', 
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
