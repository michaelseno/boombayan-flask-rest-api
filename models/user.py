from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.String(10), nullable=False, server_default="active")
    cred_id = db.Column(db.Integer, db.ForeignKey("credentials.id"), unique=False, nullable=False)

    credentials = db.relationship("CredentialModel", back_populates="users")
