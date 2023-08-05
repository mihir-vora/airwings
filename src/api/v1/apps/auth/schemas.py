from marshmallow import fields, validate, Schema

class UserSchema(Schema):
    id_ = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(max=100))
    last_name = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.Str(load_only=True, validate=validate.Length(min=8, max=20))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AdminSchema(Schema):
    id_ = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))
    role = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)