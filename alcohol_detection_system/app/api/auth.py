# app/api/auth.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.schemas.user import UserSchema
from app.extensions import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)

        if User.query.filter_by(username=user.username).first():
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User created successfully'
        }), 201
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        if user and user.check_password(data.get('password')):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'success': True,
                'data': {
                    'access_token': access_token,
                    'user_role': user.role,
                    'user_id': user.id
                }
            }), 200

        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
