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
