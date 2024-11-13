# app/utils/validators.py
import re
from typing import Optional


def validate_email(email: Optional[str]) -> bool:
    if not email:
        raise ValueError('Email is required')

    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        raise ValueError('Invalid email format')

    return True


def validate_password(password: Optional[str]) -> bool:
    if not password:
        raise ValueError('Password is required')

    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')

    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')

    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')

    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one number')

    return True


def validate_phone_number(phone: str) -> bool:
    phone_pattern = re.compile(r'^(\+84|0)[0-9]{9,10}$')
    if not phone_pattern.match(phone):
        raise ValueError('Invalid phone number format')
    return True
