# app/logging.py
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure file handler
    file_handler = RotatingFileHandler(
        'logs/alcohol_detection.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Alcohol Detection System startup')
