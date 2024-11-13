# app/schemas/violation.py
from marshmallow import Schema, fields, validate, post_load
from app.models.violation import ViolationRecord


class ViolationRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    test_id = fields.Int(required=True)
    processed_by = fields.Int(required=True)

    violation_code = fields.Str(
        required=True, validate=validate.Length(max=20))
    fine_amount = fields.Float(required=True, validate=validate.Range(min=0))
    payment_status = fields.Str(
        validate=validate.OneOf(['unpaid', 'paid', 'processing']))
    payment_deadline = fields.DateTime(allow_none=True)
    payment_date = fields.DateTime(allow_none=True)

    license_confiscated = fields.Bool()
    vehicle_detained = fields.Bool()
    additional_penalties = fields.Str()
    notes = fields.Str()

    status = fields.Str(validate=validate.OneOf(
        ['active', 'cancelled', 'completed']))
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_violation(self, data, **kwargs):
        return ViolationRecord(**data)
