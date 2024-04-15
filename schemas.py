from marshmallow import Schema, fields


class PlainCredentialSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    is_admin = fields.Bool(dump_only=True)


class CredentialDisplaySchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    is_admin = fields.Bool(dump_only=True)


class PlainBankSchema(Schema):
    id = fields.Str(dump_only=True)
    bank_name = fields.Str(required=True)
    account_number = fields.Str(required=True)
    is_active = fields.Bool(dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)


class CredentialSchema(PlainCredentialSchema):
    cred_id = fields.Int(required=True, dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    user_id = fields.Str(required=True, dump_only=True)
    credentials = fields.Nested(PlainCredentialSchema(), load_only=True)
    bank = fields.Nested(PlainBankSchema(), load_only=True)


class UserDisplaySchema(PlainUserSchema):
    user_id = fields.Str(required=True, dump_only=True)
    credentials = fields.Nested(CredentialDisplaySchema(), dump_only=True)
    banks = fields.Nested(PlainBankSchema(), dump_only=True)
