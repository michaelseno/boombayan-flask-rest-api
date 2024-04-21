from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from passlib.hash import pbkdf2_sha256

from db import db

from models import UserModel, CredentialModel, BankModel
from schemas import UserDisplaySchema, UserSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import uuid

blp = Blueprint("Admin", "admin", __name__, description="Operations on admin")


@blp.route("/admin/register")
class AdminRegister(MethodView):
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
            is_admin=True
        )
        user = UserModel(
            id=user_id,
            firstname=user_data["firstname"],
            lastname=user_data["lastname"],
            email=user_data["email"],
            phone=user_data["phone"],
            is_active=True,
            is_verified=True,
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
            abort(400, message=f"User information already exist.")
        except SQLAlchemyError as e:
            abort(500, message=f"Encountered an error while adding the user to the database.")

        return {"message": "Admin created successfully."}, 201


@blp.route("/admin/activate/<string:user_id>")
class AdminActivateUser(MethodView):
    @jwt_required()
    @blp.response(200, UserDisplaySchema)
    def put(self, user_id):
        claim = get_jwt()
        if claim["is_admin"]:
            user = UserModel.query.get(user_id)

            if user and not user.is_active:
                user.is_active = True

        else:
            abort(404, message="Need admin privilege to view all users.")

        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/admin/deactivate/<string:user_id>")
class AdminDeactivateUser(MethodView):
    @jwt_required()
    @blp.response(200, UserDisplaySchema)
    def put(self, user_id):
        claim = get_jwt()
        if claim["is_admin"]:
            user = UserModel.query.get(user_id)

            if user:
                user.is_active = False
        else:
            abort(404, message="Need admin privilege to view all users.")

        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/admin/delete/<string:user_id>")
class AdminDeleteUser(MethodView):
    @jwt_required()
    def delete(self, user_id):
        item = UserModel.query.get_or_404(user_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"User with id: {user_id} Deleted successfully"}
