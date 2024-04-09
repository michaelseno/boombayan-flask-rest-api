from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import UserModel, CredentialModel
from schemas import PlainCredentialSchema, UserSchema, PlainUserSchema

blp = Blueprint("Users", "users", __name__, description="Operations on users")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainCredentialSchema)
    def post(self, user_data):
        user = CredentialModel.query.filter(
            CredentialModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            additional_claims = {"is_admin": user.is_admin}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return {"access_token": access_token}

        abort(401, message="Invalid credentials")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainCredentialSchema)
    def post(self, user_data):
        user = CredentialModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            is_admin=True
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Encountered an error while adding the user to the database.{str(e)}")

        return {"message": "User created successfully."}, 201


@blp.route("/users")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["is_admin"]:
            return UserModel.query.all()
        else:
            abort(404, message="Need admin privilege to view all users.")


@blp.route("/user")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        claim = get_jwt()
        user = UserModel.query.get_or_404(claim["sub"])
        return user

    @jwt_required()
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        claim = get_jwt()
        user = CredentialModel.query.get_or_404(claim["sub"])
        if user:
            user_info = UserModel(
                firstname=user_data["firstname"],
                lastname=user_data["lastname"],
                email=user_data["email"],
                phone=user_data["phone"],
                cred_id=claim["sub"],
                status="active"
            )

            try:
                db.session.add(user_info)
                db.session.commit()
            except IntegrityError:
                abort(400, message="email already exists.")
            except SQLAlchemyError:
                abort(500, message="An error occurred inserting the user information to the DB.")
        return {"message": "User successfully created."}, 201

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
