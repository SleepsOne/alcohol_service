# app/utils/rate_limit.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def setup_rate_limiting(app):
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Custom limits for specific endpoints
    @limiter.limit("3 per minute")
    @app.route("/api/auth/login")
    def login():
        pass

    @limiter.limit("5 per minute")
    @app.route("/api/measurements", methods=["POST"])
    def create_measurement():
        pass
