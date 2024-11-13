# app/schemas/measurement.py
from marshmallow import Schema, fields, validate, post_load
from app.models.measurement import AlcoholTest


class AlcoholTestSchema(Schema):
    id = fields.Int(dump_only=True)
    device_id = fields.Int(required=True)
    officer_id = fields.Int(required=True)

    subject_name = fields.Str(required=True, validate=validate.Length(max=100))
    subject_id = fields.Str(required=True, validate=validate.Length(max=20))
    subject_age = fields.Int(validate=validate.Range(min=16, max=100))
    subject_gender = fields.Str(
        validate=validate.OneOf(['male', 'female', 'other']))

    alcohol_level = fields.Float(required=True, validate=validate.Range(min=0))
    violation_level = fields.Str(
        validate=validate.OneOf(['none', 'low', 'high']))
    test_time = fields.DateTime()
    location = fields.Str(validate=validate.Length(max=200))
    location_coordinates = fields.Str(validate=validate.Length(max=50))

    status = fields.Str(validate=validate.OneOf(
        ['pending', 'processed', 'cancelled']))
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_test(self, data, **kwargs):
        return AlcoholTest(**data)
