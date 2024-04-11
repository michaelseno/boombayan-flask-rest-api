from db import db


class CredentialModel(db.Model):
    __tablename__ = "credentials"

    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)
    users = db.relationship("UserModel", back_populates="credentials")



