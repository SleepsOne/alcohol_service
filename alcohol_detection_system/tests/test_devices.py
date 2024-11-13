from flask import json

# tests/test_devices.py


def test_register_device(client, auth_header):
    """Test device registration"""
    data = {
        'device_id': 'DEV-TEST-001',
        'name': 'Test Device',
        'model': 'Test Model'
    }

    response = client.post('/api/devices/register',
                           data=json.dumps(data),
                           content_type='application/json',
                           headers=auth_header)

    assert response.status_code == 201
    assert b'Device registered successfully' in response.data


def test_check_device(client, auth_header, test_device):
    """Test device status check"""
    response = client.get(f'/api/devices/check/{test_device.device_id}',
                          headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert data['exists'] == True
    assert data['device_name'] == 'Test Device'
    assert data['status'] == 'active'


def test_check_nonexistent_device(client, auth_header):
    """Test checking status of non-existent device"""
    response = client.get('/api/devices/check/NONEXISTENT',
                          headers=auth_header)

    assert response.status_code == 404
    assert response.get_json()['exists'] == False
