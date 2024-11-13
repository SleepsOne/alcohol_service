# app/models/violation.py
from app.extensions import db
from datetime import datetime


class ViolationRecord(db.Model):
    __tablename__ = 'violation_records'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('alcohol_tests.id'))
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Violation details
    violation_code = db.Column(db.String(20))
    fine_amount = db.Column(db.Float)
    # 'unpaid', 'paid', 'processing'
    payment_status = db.Column(db.String(20), default='unpaid')
    payment_deadline = db.Column(db.DateTime)
    payment_date = db.Column(db.DateTime)

    # Additional details
    license_confiscated = db.Column(db.Boolean, default=False)
    vehicle_detained = db.Column(db.Boolean, default=False)
    additional_penalties = db.Column(db.Text)
    notes = db.Column(db.Text)

    # 'active', 'cancelled', 'completed'
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'test_id': self.test_id,
            'processed_by': self.processed_by,
            'violation_code': self.violation_code,
            'fine_amount': self.fine_amount,
            'payment_status': self.payment_status,
            'payment_deadline': self.payment_deadline.isoformat() if self.payment_deadline else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'license_confiscated': self.license_confiscated,
            'vehicle_detained': self.vehicle_detained,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
