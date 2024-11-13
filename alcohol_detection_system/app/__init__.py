# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, migrate
from app.config import config_by_name
from app.config import config_by_name, CustomJSONEncoder


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.json_encoder = CustomJSONEncoder

    # Thêm logging để debug
    app.logger.info(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

    try:
        # Initialize extensions
        db.init_app(app)
        jwt.init_app(app)
        migrate.init_app(app, db)
        CORS(app)

        # Test database connection
        with app.app_context():
            db.engine.connect()
            app.logger.info("Database connection successful")

    except Exception as e:
        app.logger.error(f"Error initializing app: {str(e)}")
        raise

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.devices import devices_bp
    from app.api.measurements import measurements_bp
    from app.api.statistics import statistics_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(measurements_bp, url_prefix='/api/measurements')
    app.register_blueprint(statistics_bp, url_prefix='/api/statistics')

    return app
