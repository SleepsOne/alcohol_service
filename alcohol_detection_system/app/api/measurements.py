# app/api/measurements.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.measurement import AlcoholTest
from app.schemas.measurement import AlcoholTestSchema
from app.services.violation_service import ViolationService  # Sửa đổi import
from app.extensions import db

measurements_bp = Blueprint('measurements', __name__)


@measurements_bp.route('', methods=['POST'])
@jwt_required()
def create_measurement():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        measurement_schema = AlcoholTestSchema()
        measurement = measurement_schema.load(
            {**data, 'officer_id': current_user})

        # Sử dụng ViolationService
        violation_level = ViolationService.process_violation(
            measurement.alcohol_level)
        measurement.violation_level = violation_level

        db.session.add(measurement)
        db.session.commit()

        # Tạo biên bản vi phạm nếu cần
        if violation_level != 'none':
            ViolationService.create_violation(measurement)

        return jsonify(measurement_schema.dump(measurement)), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@measurements_bp.route('', methods=['GET'])
@jwt_required()
def get_measurements():
    try:
        measurements = AlcoholTest.query.all()
        measurement_schema = AlcoholTestSchema(many=True)
        return jsonify(measurement_schema.dump(measurements)), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
