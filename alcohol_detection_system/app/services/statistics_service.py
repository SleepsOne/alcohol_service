# app/services/statistics_service.py
from datetime import datetime, timedelta
from sqlalchemy import func
from app.extensions import db
from app.models.measurement import AlcoholTest
from app.models.violation import ViolationRecord


class StatisticsService:
    @staticmethod
    def generate_statistics(time_range='week'):
        """
        Tạo thống kê dựa trên khoảng thời gian
        time_range: 'week', 'month', 'year'
        """
        # Xác định thời gian bắt đầu dựa trên time_range
        if time_range == 'week':
            start_date = datetime.utcnow() - timedelta(days=7)
        elif time_range == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
        elif time_range == 'year':
            start_date = datetime.utcnow() - timedelta(days=365)
        else:
            start_date = datetime.utcnow() - timedelta(days=7)

        # Truy vấn cơ bản
        measurements = AlcoholTest.query.filter(
            AlcoholTest.created_at >= start_date
        ).all()

        violations = ViolationRecord.query.filter(
            ViolationRecord.created_at >= start_date
        ).all()

        # Tính toán thống kê
        stats = {
            'total_tests': len(measurements),
            'total_violations': len(violations),
            'violation_levels': {
                'none': len([m for m in measurements if m.violation_level == 'none']),
                'low': len([m for m in measurements if m.violation_level == 'low']),
                'high': len([m for m in measurements if m.violation_level == 'high'])
            },
            'total_fines': sum(v.fine_amount for v in violations),
            'paid_fines': sum(v.fine_amount for v in violations if v.payment_status == 'paid'),
            'age_distribution': StatisticsService._calculate_age_distribution(measurements),
            'time_distribution': StatisticsService._calculate_time_distribution(measurements),
            'location_distribution': StatisticsService._calculate_location_distribution(measurements)
        }

        return stats

    @staticmethod
    def _calculate_age_distribution(measurements):
        """Tính phân bố độ tuổi của người vi phạm"""
        age_ranges = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-55': 0,
            '55+': 0
        }

        for m in measurements:
            if m.subject_age <= 25:
                age_ranges['18-25'] += 1
            elif m.subject_age <= 35:
                age_ranges['26-35'] += 1
            elif m.subject_age <= 45:
                age_ranges['36-45'] += 1
            elif m.subject_age <= 55:
                age_ranges['46-55'] += 1
            else:
                age_ranges['55+'] += 1

        return age_ranges

    @staticmethod
    def _calculate_time_distribution(measurements):
        """Tính phân bố thời gian vi phạm"""
        time_ranges = {
            'morning': 0,    # 6-12
            'afternoon': 0,  # 12-18
            'evening': 0,    # 18-24
            'night': 0       # 0-6
        }

        for m in measurements:
            hour = m.created_at.hour
            if 6 <= hour < 12:
                time_ranges['morning'] += 1
            elif 12 <= hour < 18:
                time_ranges['afternoon'] += 1
            elif 18 <= hour < 24:
                time_ranges['evening'] += 1
            else:
                time_ranges['night'] += 1

        return time_ranges

    @staticmethod
    def _calculate_location_distribution(measurements):
        """Tính phân bố địa điểm vi phạm"""
        locations = {}
        for m in measurements:
            if m.location:
                locations[m.location] = locations.get(m.location, 0) + 1

        return dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10])


def generate_statistics(time_range='week'):
    """Helper function để gọi service dễ dàng hơn"""
    return StatisticsService.generate_statistics(time_range)
