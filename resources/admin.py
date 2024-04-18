from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from db import db

from models import UserModel
from schemas import UserDisplaySchema

import uuid

blp = Blueprint("Admin", "admin", __name__, description="Operations on admin")


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
