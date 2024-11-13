# app/services/violation_service.py
from datetime import datetime, timedelta
from app.extensions import db
from app.models.violation import ViolationRecord


class ViolationService:
    VIOLATION_CODES = {
        'low': 'ALC001',   # 0.2 - 0.4 mg/L
        'high': 'ALC002'   # > 0.4 mg/L
    }

    FINE_AMOUNTS = {
        'low': 2500000,    # VND
        'high': 5000000    # VND
    }

    @staticmethod
    def process_violation(alcohol_level: float) -> str:
        """
        Xác định mức độ vi phạm dựa trên nồng độ cồn
        """
        if alcohol_level < 0.2:
            return 'none'
        elif alcohol_level <= 0.4:
            return 'low'
        else:
            return 'high'

    @staticmethod
    def create_violation(measurement):
        """
        Tạo biên bản vi phạm dựa trên kết quả đo
        """
        if measurement.violation_level == 'none':
            return None

        violation = ViolationRecord(
            test_id=measurement.id,
            processed_by=measurement.officer_id,
            violation_code=ViolationService.VIOLATION_CODES[measurement.violation_level],
            fine_amount=ViolationService.FINE_AMOUNTS[measurement.violation_level],
            payment_deadline=datetime.utcnow() + timedelta(days=30),
            license_confiscated=measurement.violation_level == 'high',
            vehicle_detained=measurement.violation_level == 'high'
        )

        db.session.add(violation)
        db.session.commit()
        return violation

    @staticmethod
    def get_violation_statistics(start_date=None, end_date=None):
        """
        Lấy thống kê vi phạm
        """
        query = ViolationRecord.query

        if start_date:
            query = query.filter(ViolationRecord.created_at >= start_date)
        if end_date:
            query = query.filter(ViolationRecord.created_at <= end_date)

        violations = query.all()

        return {
            'total': len(violations),
            'by_level': {
                'low': len([v for v in violations if v.violation_code == 'ALC001']),
                'high': len([v for v in violations if v.violation_code == 'ALC002'])
            },
            'total_fines': sum(v.fine_amount for v in violations),
            'paid_fines': sum(v.fine_amount for v in violations if v.payment_status == 'paid')
        }
