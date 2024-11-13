# app/models/measurement.py
from app.extensions import db
from datetime import datetime


class AlcoholTest(db.Model):
    __tablename__ = 'alcohol_tests'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    officer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Subject information
    subject_name = db.Column(db.String(100))
    subject_id = db.Column(db.String(20))  # CMND/CCCD
    subject_age = db.Column(db.Integer)
    subject_gender = db.Column(db.String(10))

    # Test details
    alcohol_level = db.Column(db.Float)
    violation_level = db.Column(db.String(20))  # 'none', 'low', 'high'
    test_time = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200))
    location_coordinates = db.Column(db.String(50))  # "latitude,longitude"

    # Additional information
    notes = db.Column(db.Text)
    # 'pending', 'processed', 'cancelled'
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    violation_record = db.relationship(
        'ViolationRecord', backref='test', lazy=True, uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'officer_id': self.officer_id,
            'subject_name': self.subject_name,
            'subject_id': self.subject_id,
            'subject_age': self.subject_age,
            'alcohol_level': self.alcohol_level,
            'violation_level': self.violation_level,
            'test_time': self.test_time.isoformat(),
            'location': self.location,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
