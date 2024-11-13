# app/utils/error_handlers.py
from flask import app, jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from jwt.exceptions import PyJWTError


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'Insufficient permissions'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({
            'error': 'Database Error',
            'message': 'Data integrity violation'
        }), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while accessing the database'
        }), 500

    @app.errorhandler(PyJWTError)
    def handle_jwt_error(error):
        return jsonify({
            'error': 'Authentication Error',
            'message': str(error)
        }), 401

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

# Middleware để log errors


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())


@app.after_request
def log_response_info(response):
    app.logger.info('Response: %s', response.get_data())
    return response
