# app/api/statistics.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.statistics_service import generate_statistics

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/', methods=['GET'])
@jwt_required()
def get_statistics():
    try:
        time_range = request.args.get(
            'range', 'week')  # 'week', 'month', 'year'
        stats = generate_statistics(time_range)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@statistics_bp.route('/violations', methods=['GET'])
@jwt_required()
def get_violation_statistics():
    try:
        from app.services.violation_service import ViolationService
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        stats = ViolationService.get_violation_statistics(start_date, end_date)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
