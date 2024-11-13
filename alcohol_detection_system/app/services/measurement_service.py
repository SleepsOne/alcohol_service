# app/services/measurement_service.py
from app.models.measurement import AlcoholTest
from app.models.device import Device
from app.services.violation_service import ViolationService
from app.extensions import db
from datetime import datetime


class MeasurementService:
    @staticmethod
    def create_measurement(data, officer_id):
        device = Device.query.filter_by(device_id=data['device_id']).first()
        if not device or device.status != 'active':
            raise ValueError('Invalid or inactive device')

        measurement = AlcoholTest(
            device_id=device.id,
            officer_id=officer_id,
            subject_name=data['subject_name'],
            subject_id=data['subject_id'],
            subject_age=data['subject_age'],
            subject_gender=data.get('subject_gender'),
            alcohol_level=data['alcohol_level'],
            test_time=datetime.utcnow(),
            location=data['location'],
            location_coordinates=data.get('location_coordinates')
        )

        # Determine violation level
        if measurement.alcohol_level < 0.2:
            measurement.violation_level = 'none'
        elif measurement.alcohol_level <= 0.4:
            measurement.violation_level = 'low'
        else:
            measurement.violation_level = 'high'

        db.session.add(measurement)
        db.session.commit()

        # Create violation record if applicable
        if measurement.violation_level != 'none':
            ViolationService.create_violation(measurement)

        return measurement

    @staticmethod
    def get_measurements_statistics(start_date=None, end_date=None):
        query = AlcoholTest.query

        if start_date:
            query = query.filter(AlcoholTest.test_time >= start_date)
        if end_date:
            query = query.filter(AlcoholTest.test_time <= end_date)

        results = query.all()

        return {
            'total_tests': len(results),
            'violations': len([r for r in results if r.violation_level != 'none']),
            'average_level': sum(r.alcohol_level for r in results) / len(results) if results else 0,
            'by_level': {
                'none': len([r for r in results if r.violation_level == 'none']),
                'low': len([r for r in results if r.violation_level == 'low']),
                'high': len([r for r in results if r.violation_level == 'high'])
            }
        }
