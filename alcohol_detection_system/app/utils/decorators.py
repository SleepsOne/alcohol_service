# app/utils/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.role != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403

        return fn(*args, **kwargs)
    return wrapper


def officer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.role not in ['admin', 'officer']:
            return jsonify({'message': 'Officer privileges required'}), 403

        return fn(*args, **kwargs)
    return wrapper
