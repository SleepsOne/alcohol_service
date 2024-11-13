# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Device, AlcoholTest, ViolationRecord
from flask_jwt_extended import create_access_token


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_header(app):
    with app.app_context():
        # Create test user
        user = User(
            username='test_officer',
            email='test@example.com',
            full_name='Test Officer',
            role='officer'
        )
        user.password = 'Test123!'
        db.session.add(user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=user.id)
        headers = {'Authorization': f'Bearer {access_token}'}

        return headers


@pytest.fixture
def test_device(app):
    with app.app_context():
        device = Device(
            device_id='TEST-DEVICE-001',
            name='Test Device',
            model='Test Model',
            status='active',
            registered_by=1
        )
        db.session.add(device)
        db.session.commit()
        return device


@pytest.fixture
def test_measurement(app, test_device):
    with app.app_context():
        measurement = AlcoholTest(
            device_id=test_device.id,
            officer_id=1,
            subject_name='Test Subject',
            subject_id='123456789',
            subject_age=30,
            alcohol_level=0.35,
            violation_level='low',
            location='Test Location'
        )
        db.session.add(measurement)
        db.session.commit()
        return measurement
