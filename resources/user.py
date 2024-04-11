from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import UserModel, CredentialModel, BankModel
from schemas import PlainCredentialSchema, UserSchema, UserDisplaySchema

import uuid

blp = Blueprint("Users", "users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        cred_id = uuid.uuid4().hex
        bank_id = uuid.uuid4().hex
        credentials = user_data["credentials"]
        banks = user_data["bank"]
        credential = CredentialModel(
            id=cred_id,
            username=credentials["username"],
            password=pbkdf2_sha256.hash(credentials["password"]),
            is_admin=True
        )
        user = UserModel(
            firstname=user_data["firstname"],
            lastname=user_data["lastname"],
            email=user_data["email"],
            phone=user_data["phone"],
            status="inactive",
            cred_id=cred_id,
            bank_id=bank_id
        )

        bank = BankModel(
            id=bank_id,
            bank_name=banks["bank_name"],
            account_number=banks["account_number"],
            is_active=True
        )

        try:
            db.session.add(credential)
            db.session.add(user)
            db.session.add(bank)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=f"User information already exist. \n{str(e)}")
        except SQLAlchemyError as e:
            abort(500, message=f"Encountered an error while adding the user to the database.\n{str(e)}")

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainCredentialSchema)
    def post(self, user_data):
        credential = CredentialModel.query.filter(
            CredentialModel.username == user_data["username"]
        ).first()

        if credential and pbkdf2_sha256.verify(user_data["password"], credential.password):
            additional_claims = {"is_admin": credential.is_admin}
            access_token = create_access_token(identity=credential.id, additional_claims=additional_claims)
            return {"access_token": access_token}

        abort(401, message="Invalid credentials")


@blp.route("/users")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserDisplaySchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["is_admin"]:
            return UserModel.query.all()
        else:
            abort(404, message="Need admin privilege to view all users.")


@blp.route("/user")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserDisplaySchema)
    def get(self):
        claim = get_jwt()
        user = UserModel.query.filter(
            UserModel.cred_id == claim["sub"]
        ).first()

        if user:
            user = UserModel.query.get_or_404(user.id)
            return user

    @jwt_required()
    def delete(self):
        claim = get_jwt()
        if claim["is_admin"]:
            user = UserModel.query.filter(
                UserModel.cred_id == claim["sub"]
            ).first()
            user = UserModel.query.get_or_404(user.id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
