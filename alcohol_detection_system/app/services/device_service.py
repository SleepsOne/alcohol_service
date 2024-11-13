# app/services/device_service.py
from app.models.device import Device
from app.extensions import db
from datetime import datetime, timedelta


class DeviceService:
    @staticmethod
    def register_device(data, user_id):
        if Device.query.filter_by(device_id=data['device_id']).first():
            raise ValueError('Device ID already registered')

        device = Device(
            device_id=data['device_id'],
            name=data['name'],
            model=data.get('model'),
            registered_by=user_id,
            last_calibration=datetime.utcnow(),
            next_calibration=datetime.utcnow() + timedelta(days=180)
        )

        db.session.add(device)
        db.session.commit()
        return device

    @staticmethod
    def check_device_status(device_id):
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            raise ValueError('Device not found')

        needs_calibration = device.next_calibration and device.next_calibration <= datetime.utcnow()

        return {
            'device': device,
            'status': device.status,
            'needs_calibration': needs_calibration,
            'days_until_calibration': (device.next_calibration - datetime.utcnow()).days if device.next_calibration else None
        }
