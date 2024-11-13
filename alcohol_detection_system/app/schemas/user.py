# app/schemas/user.py
from marshmallow import Schema, fields, validate, post_load
from app.models.user import User


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, load_only=True,
                          validate=validate.Length(min=6))
    full_name = fields.Str(validate=validate.Length(max=120))
    email = fields.Email()
    role = fields.Str(validate=validate.OneOf(['admin', 'officer', 'user']))
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
