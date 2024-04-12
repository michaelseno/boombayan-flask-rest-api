from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(), primary_key=True)
    firstname = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(), unique=False, nullable=False)
    is_verified = db.Column(db.Boolean(), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    cred_id = db.Column(db.String(), db.ForeignKey("credentials.id"), unique=True, nullable=False)
    bank_id = db.Column(db.String(), db.ForeignKey("banks.id"), unique=True, nullable=False)

    banks = db.relationship("BankModel", back_populates="users", cascade="all, delete")
    credentials = db.relationship("CredentialModel", back_populates="users", cascade="all, delete")
