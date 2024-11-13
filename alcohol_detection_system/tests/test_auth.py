# tests/test_auth.py
import pytest
from flask import json


def test_register_user(client):
    """Test user registration"""
    data = {
        'username': 'newuser',
        'password': 'SecurePass123!',
        'email': 'newuser@example.com',
        'full_name': 'New User',
        'role': 'officer'
    }

    response = client.post('/api/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')

    assert response.status_code == 201
    assert b'User created successfully' in response.data


def test_register_duplicate_username(client):
    """Test registration with existing username"""
    # First registration
    data = {
        'username': 'duplicate_user',
        'password': 'SecurePass123!',
        'email': 'user1@example.com'
    }

    client.post('/api/auth/register',
                data=json.dumps(data),
                content_type='application/json')

    # Second registration with same username
    data['email'] = 'user2@example.com'
    response = client.post('/api/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')

    assert response.status_code == 400
    assert b'Username already exists' in response.data


def test_login_success(client):
    """Test successful login"""
    # Register user
    register_data = {
        'username': 'loginuser',
        'password': 'SecurePass123!',
        'email': 'loginuser@example.com'
    }

    client.post('/api/auth/register',
                data=json.dumps(register_data),
                content_type='application/json')

    # Login
    login_data = {
        'username': 'loginuser',
        'password': 'SecurePass123!'
    }

    response = client.post('/api/auth/login',
                           data=json.dumps(login_data),
                           content_type='application/json')

    assert response.status_code == 200
    assert 'access_token' in response.get_json()
