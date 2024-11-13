from flask import json

# tests/test_measurements.py


def test_create_measurement(client, auth_header, test_device):
    """Test creating new measurement"""
    data = {
        'device_id': test_device.device_id,
        'subject_name': 'Test Subject',
        'subject_id': '123456789',
        'subject_age': 30,
        'alcohol_level': 0.35,
        'location': 'Test Location'
    }

    response = client.post('/api/measurements/',
                           data=json.dumps(data),
                           content_type='application/json',
                           headers=auth_header)

    assert response.status_code == 201
    data = response.get_json()
    assert data['violation_level'] == 'low'
    assert 'fine_amount' in data


def test_get_measurements(client, auth_header, test_measurement):
    """Test getting measurement list"""
    response = client.get('/api/measurements/',
                          headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_measurement_violation_processing(client, auth_header, test_device):
    """Test violation processing for high alcohol level"""
    data = {
        'device_id': test_device.device_id,
        'subject_name': 'Violation Test',
        'subject_id': '987654321',
        'subject_age': 25,
        'alcohol_level': 0.45,  # High level
        'location': 'Test Location'
    }

    response = client.post('/api/measurements/',
                           data=json.dumps(data),
                           content_type='application/json',
                           headers=auth_header)

    assert response.status_code == 201
    data = response.get_json()
    assert data['violation_level'] == 'high'
    assert data['fine_amount'] > 0


def test_statistics(client, auth_header, test_measurement):
    """Test getting measurement statistics"""
    response = client.get('/api/statistics/',
                          headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert 'total_tests' in data
    assert 'violation_tests' in data
    assert 'age_distribution' in data
    assert 'violation_distribution' in data
