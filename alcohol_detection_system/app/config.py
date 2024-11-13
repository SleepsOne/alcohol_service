# app/config.py
import os
from datetime import timedelta
from flask.json import JSONEncoder
from datetime import datetime


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class Config:
    SECRET_KEY = os.getenv(
        'SECRET_KEY', 'fde5e9578f09002da094622def431cee6e3142c75c9117d2')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:1@localhost:5432/alcohol_detection_db')

    # Thêm các options cho SQLAlchemy
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY', '206624349d96f11f7b78262f21fbdc6582f8973686d3f921')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # JSON configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
