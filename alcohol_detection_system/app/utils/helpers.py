# app/utils/helpers.py
import uuid
from datetime import datetime
import locale
from typing import Union, Optional


def generate_device_id() -> str:
    """Generate a unique device ID"""
    return f'DEV-{uuid.uuid4().hex[:8].upper()}'


def format_currency(amount: Union[int, float]) -> str:
    """Format amount in VND currency"""
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    return locale.currency(amount, grouping=True, symbol='₫')


def format_datetime(dt: datetime, format_str: Optional[str] = None) -> str:
    """Format datetime object to string"""
    if not format_str:
        format_str = '%d/%m/%Y %H:%M:%S'
    return dt.strftime(format_str)


def parse_coordinates(coordinates_str: str) -> tuple:
    """Parse coordinates string to tuple of floats"""
    try:
        lat, lon = map(float, coordinates_str.split(','))
        return lat, lon
    except (ValueError, AttributeError):
        raise ValueError(
            'Invalid coordinates format. Expected "latitude,longitude"')


def calculate_age(birth_date: str) -> int:
    """Calculate age from birth date string (DD/MM/YYYY)"""
    try:
        birth = datetime.strptime(birth_date, '%d/%m/%Y')
        today = datetime.today()
        age = today.year - birth.year - \
            ((today.month, today.day) < (birth.month, birth.day))
        return age
    except ValueError:
        raise ValueError('Invalid birth date format. Expected DD/MM/YYYY')
