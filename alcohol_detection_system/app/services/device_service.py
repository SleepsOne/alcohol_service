# app/services/device_service.py
from app.models.device import Device
from app.extensions import db
from datetime import datetime, timedelta
from sqlalchemy import or_


class DeviceService:
    @staticmethod
    def register_device(data, user_id):
        if Device.query.filter_by(device_id=data['device_id']).first():
            raise ValueError('Device ID already registered')

        device = Device(
            device_id=data['device_id'],
            name=data['name'],
            model=data.get('model'),
            registered_by=user_id,
            last_calibration=datetime.utcnow(),
            next_calibration=datetime.utcnow() + timedelta(days=180)
        )

        db.session.add(device)
        db.session.commit()
        return device

    @staticmethod
    def check_device_status(device_id):
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            raise ValueError('Device not found')

        needs_calibration = device.next_calibration and device.next_calibration <= datetime.utcnow()

        return {
            'device': device,
            'status': device.status,
            'needs_calibration': needs_calibration,
            'days_until_calibration': (device.next_calibration - datetime.utcnow()).days if device.next_calibration else None
        }

    @staticmethod
    def get_all_devices(filters=None, page=1, per_page=10):
        """
        Lấy danh sách thiết bị với các bộ lọc và phân trang

        Args:
            filters (dict): Các điều kiện lọc (status, search)
            page (int): Số trang
            per_page (int): Số items mỗi trang

        Returns:
            dict: Danh sách thiết bị và thông tin phân trang
        """
        try:
            # Bắt đầu query
            query = Device.query

            if filters:
                # Lọc theo status
                if filters.get('status'):
                    query = query.filter(Device.status == filters['status'])

                # Tìm kiếm theo name hoặc device_id
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Device.name.ilike(search_term),
                            Device.device_id.ilike(search_term)
                        )
                    )

            # Get total count trước khi phân trang
            total_count = query.count()

            # Apply sorting và pagination
            devices = query.order_by(Device.created_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)

            return {
                'devices': devices.items,
                'pagination': {
                    'total_items': total_count,
                    'total_pages': devices.pages,
                    'current_page': page,
                    'per_page': per_page,
                    'has_next': devices.has_next,
                    'has_prev': devices.has_prev
                }
            }
        except Exception as e:
            raise ValueError(f'Error getting devices: {str(e)}')

    @staticmethod
    def update_device_status(device_id, status):
        """
        Cập nhật trạng thái thiết bị
        """
        try:
            device = Device.query.filter_by(device_id=device_id).first()
            if not device:
                raise ValueError('Device not found')

            device.status = status
            db.session.commit()
            return device
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error updating device status: {str(e)}')

    @staticmethod
    def update_calibration(device_id):
        """
        Cập nhật thông tin hiệu chuẩn của thiết bị
        """
        try:
            device = Device.query.filter_by(device_id=device_id).first()
            if not device:
                raise ValueError('Device not found')

            device.last_calibration = datetime.utcnow()
            device.next_calibration = datetime.utcnow() + timedelta(days=180)
            db.session.commit()
            return device
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error updating calibration: {str(e)}')

    @staticmethod
    def get_devices_need_calibration():
        """
        Lấy danh sách thiết bị cần hiệu chuẩn
        """
        try:
            return Device.query.filter(
                Device.next_calibration <= datetime.utcnow()
            ).all()
        except Exception as e:
            raise ValueError(
                f'Error getting devices need calibration: {str(e)}')

    @staticmethod
    def get_device_statistics():
        """
        Lấy thống kê về thiết bị
        """
        try:
            total_devices = Device.query.count()
            active_devices = Device.query.filter_by(status='active').count()
            maintenance_devices = Device.query.filter_by(
                status='maintenance').count()
            devices_need_calibration = Device.query.filter(
                Device.next_calibration <= datetime.utcnow()
            ).count()

            return {
                'total_devices': total_devices,
                'active_devices': active_devices,
                'maintenance_devices': maintenance_devices,
                'devices_need_calibration': devices_need_calibration
            }
        except Exception as e:
            raise ValueError(f'Error getting device statistics: {str(e)}')

    # Thêm
    @staticmethod
    def delete_device(device_id):
        try:
            device = Device.query.filter_by(device_id=device_id).first()
            if not device:
                raise ValueError('Device not found')

            db.session.delete(device)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error deleting device: {str(e)}')

    @staticmethod
    def update_device(device_id, data):
        try:
            device = Device.query.filter_by(device_id=device_id).first()
            if not device:
                raise ValueError('Device not found')

            # Update các trường được cho phép
            allowed_fields = ['name', 'model', 'status']
            for field in allowed_fields:
                if field in data:
                    setattr(device, field, data[field])

            db.session.commit()
            return device
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error updating device: {str(e)}')

    @staticmethod
    def get_device_by_id(device_id):
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            raise ValueError('Device not found')
        return device
