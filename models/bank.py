from db import db


class BankModel(db.Model):
    __tablename__ = "banks"

    id = db.Column(db.String(), primary_key=True)
    bank_name = db.Column(db.String(80), unique=False, nullable=False)
    account_number = db.Column(db.String(15), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    users = db.relationship("UserModel", back_populates="banks")

