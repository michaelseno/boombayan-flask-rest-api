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
        user_id = uuid.uuid4().hex
        cred_id = uuid.uuid4().hex
        bank_id = uuid.uuid4().hex
        credentials = user_data["credentials"]
        banks = user_data["bank"]
        credential = CredentialModel(
            id=cred_id,
            username=credentials["username"],
            password=pbkdf2_sha256.hash(credentials["password"]),
            is_admin=False
        )
        user = UserModel(
            id=user_id,
            firstname=user_data["firstname"],
            lastname=user_data["lastname"],
            email=user_data["email"],
            phone=user_data["phone"],
            is_active=False,
            is_verified=False,
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
        user_info = CredentialModel.query.filter(
            CredentialModel.username == user_data["username"]
        ).first()

        if user_info and pbkdf2_sha256.verify(user_data["password"], user_info.password):
            if user_info.users[0].is_active:
                additional_claims = {"is_admin": user_info.is_admin}
                access_token = create_access_token(identity=user_info.users[0].id, additional_claims=additional_claims)
                return {"access_token": access_token}
            else:
                abort(404, message="Failed to login due to account is not active.")

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


@blp.route("/user/<string:user_id>")
class UserDetail(MethodView):
    @jwt_required()
    @blp.response(200, UserDisplaySchema)
    def get(self, user_id):
        claim = get_jwt()
        if claim["is_admin"]:
            try:
                return UserModel.query.get_or_404(user_id)
            except SQLAlchemyError:
                abort(500, message="Encountered an error retrieving data.")
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


@blp.route("/user/<string:user_id>/verify")
class UserVerify(MethodView):

    def put(self, user_id):
        try:
            user = UserModel.query.get(user_id)

            if user and not user.is_verified:
                user.is_verified = True

            db.session.add(user)
            db.session.commit()
            return {"message": "account successfully verified."}, 200

        except SQLAlchemyError:
            abort(500, message="Encountered an error retrieving data.")
