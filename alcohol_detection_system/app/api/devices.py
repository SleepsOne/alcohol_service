# app/api/devices.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.device_service import DeviceService
from app.models.device import Device
from app.schemas.device import DeviceSchema
from app.extensions import db

devices_bp = Blueprint('devices', __name__)


@devices_bp.route('/register', methods=['POST'])
@jwt_required()
def register_device():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        device_schema = DeviceSchema()
        device = device_schema.load({**data, 'registered_by': current_user})

        if Device.query.filter_by(device_id=device.device_id).first():
            return jsonify({'message': 'Device already registered'}), 400

        db.session.add(device)
        db.session.commit()

        return jsonify({'message': 'Device registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@devices_bp.route('/check/<device_id>', methods=['GET'])
@jwt_required()
def check_device(device_id):
    device = Device.query.filter_by(device_id=device_id).first()
    if not device:
        return jsonify({'exists': False}), 404

    return jsonify({
        'exists': True,
        'device_name': device.name,
        'status': device.status
    }), 200


@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_devices():
    try:
        # Get query parameters
        filters = {
            'status': request.args.get('status'),
            'search': request.args.get('search')
        }
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Use service to get devices
        result = DeviceService.get_all_devices(filters, page, per_page)

        # Serialize data
        device_schema = DeviceSchema(many=True)
        devices_data = device_schema.dump(result['devices'])

        return jsonify({
            'success': True,
            'data': {
                'devices': devices_data,
                'pagination': result['pagination']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
