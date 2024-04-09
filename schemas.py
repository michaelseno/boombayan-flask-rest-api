from marshmallow import Schema, fields


class PlainCredentialSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    is_admin = fields.Bool(dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Int(required=True)
    status = fields.Str(dump_only=True)


class CredentialSchema(PlainCredentialSchema):
    cred_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    user_id = fields.Int(required=True, load_only=True)
    credentials = fields.Nested(PlainCredentialSchema(), dump_only=True)


