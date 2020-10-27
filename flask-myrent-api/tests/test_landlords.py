


def test_get_landlords_no_records(client):
    response = client.get('/api/v1/landlords')
    expected_result = {
        'success': True,
        'data': []
    }
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_landlords_sample_data(client, sample_data):
    pass
