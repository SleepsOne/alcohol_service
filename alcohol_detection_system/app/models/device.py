# app/models/device.py
from app.extensions import db
from datetime import datetime


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    model = db.Column(db.String(50))
    # 'active', 'inactive', 'maintenance'
    status = db.Column(db.String(20), default='active')
    last_calibration = db.Column(db.DateTime)
    next_calibration = db.Column(db.DateTime)
    registered_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    measurements = db.relationship('AlcoholTest', backref='device', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'name': self.name,
            'model': self.model,
            'status': self.status,
            'last_calibration': self.last_calibration.isoformat() if self.last_calibration else None,
            'next_calibration': self.next_calibration.isoformat() if self.next_calibration else None,
            'registered_by': self.registered_by,
            'created_at': self.created_at.isoformat()
        }
