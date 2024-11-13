# app/services/auth_service.py
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.utils.validators import validate_email, validate_password


class AuthService:
    @staticmethod
    def register_user(data):
        validate_email(data.get('email'))
        validate_password(data.get('password'))

        if User.query.filter_by(username=data['username']).first():
            raise ValueError('Username already exists')

        if User.query.filter_by(email=data['email']).first():
            raise ValueError('Email already exists')

        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name'),
            role=data.get('role', 'user')
        )
        user.password = data['password']

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            raise ValueError('Invalid credentials')

        if user.status != 'active':
            raise ValueError('Account is not active')

        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        return {'token': access_token, 'user': user}
