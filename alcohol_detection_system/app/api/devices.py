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

# 1. API cập nhật trạng thái thiết bị


@devices_bp.route('/<device_id>/status', methods=['PUT'])
@jwt_required()
def update_device_status(device_id):
    try:
        data = request.get_json()
        if 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Status is required'
            }), 400

        device = DeviceService.update_device_status(device_id, data['status'])
        device_schema = DeviceSchema()

        return jsonify({
            'success': True,
            'message': 'Device status updated successfully',
            'data': device_schema.dump(device)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 2. API cập nhật thông tin hiệu chuẩn


@devices_bp.route('/<device_id>/calibration', methods=['POST'])
@jwt_required()
def update_device_calibration(device_id):
    try:
        device = DeviceService.update_calibration(device_id)
        device_schema = DeviceSchema()

        return jsonify({
            'success': True,
            'message': 'Device calibration updated successfully',
            'data': device_schema.dump(device)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 3. API lấy danh sách thiết bị cần hiệu chuẩn


@devices_bp.route('/calibration/needed', methods=['GET'])
@jwt_required()
def get_devices_need_calibration():
    try:
        devices = DeviceService.get_devices_need_calibration()
        device_schema = DeviceSchema(many=True)

        return jsonify({
            'success': True,
            'data': device_schema.dump(devices)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 4. API lấy thống kê thiết bị


@devices_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_device_statistics():
    try:
        stats = DeviceService.get_device_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 5. API xóa thiết bị (thêm mới vào service)


@devices_bp.route('/<device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    try:
        DeviceService.delete_device(device_id)
        return jsonify({
            'success': True,
            'message': 'Device deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 6. API cập nhật thông tin thiết bị


@devices_bp.route('/<device_id>', methods=['PUT'])
@jwt_required()
def update_device(device_id):
    try:
        data = request.get_json()
        device_schema = DeviceSchema(partial=True)
        updated_device = DeviceService.update_device(device_id, data)

        return jsonify({
            'success': True,
            'message': 'Device updated successfully',
            'data': device_schema.dump(updated_device)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# 7. API lấy chi tiết thiết bị


@devices_bp.route('/<device_id>', methods=['GET'])
@jwt_required()
def get_device_details(device_id):
    try:
        device = DeviceService.get_device_by_id(device_id)
        device_schema = DeviceSchema()

        return jsonify({
            'success': True,
            'data': device_schema.dump(device)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
