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


class FundUpdateSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    fund_type = fields.Str(nullable=False)
    total_fund = fields.Float(nullable=False)
    last_updated = fields.DateTime(nullable=False, dump_only=True)
    updated_by = fields.Str(nullable=False, dump_only=True)
    remarks = fields.Str(nullable=False)


class FundDisplaySchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    fund_type = fields.Str(nullable=False)
    total_fund = fields.Float(nullable=False)
    last_updated = fields.DateTime(nullable=False)
    updated_by = fields.Str(nullable=False)
    remarks = fields.Str(nullable=False)


class LoanDisplaySchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    user_id = fields.Str(nullable=False)
    loan_amount = fields.Float(nullable=False)
    payment_term = fields.Int(nullable=False)
    date_applied = fields.DateTime(nullable=False)
    first_approve = fields.Str()
    date_first_approve = fields.DateTime()
    second_approve = fields.Str()
    date_second_approve = fields.DateTime()
    is_approved = fields.Bool(dump_only=True)


class ApplyLoanSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    user_id = fields.Str(nullable=False)
    loan_amount = fields.Float(nullable=False)
    payment_term = fields.Int(nullable=False)
