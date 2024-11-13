# app/schemas/device.py
from marshmallow import Schema, fields, validate, post_load
from app.models.device import Device


class DeviceSchema(Schema):
    id = fields.Int(dump_only=True)
    device_id = fields.Str(required=True, validate=validate.Length(max=100))
    name = fields.Str(validate=validate.Length(max=100))
    model = fields.Str(validate=validate.Length(max=50))
    status = fields.Str(validate=validate.OneOf(
        ['active', 'inactive', 'maintenance']))
    last_calibration = fields.DateTime(allow_none=True)
    next_calibration = fields.DateTime(allow_none=True)
    registered_by = fields.Int()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_device(self, data, **kwargs):
        return Device(**data)
