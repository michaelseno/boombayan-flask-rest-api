from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import FundModel, UserModel
from schemas import FundDisplaySchema, FundUpdateSchema

import uuid
import datetime

blp = Blueprint("Fund", "fund", __name__, description="Operations on fund")


@blp.route("/fund")
class ManageFund(MethodView):
    @jwt_required()
    @blp.response(200, FundDisplaySchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["is_admin"]:
            return FundModel.query.all()
        else:
            abort(404, message="Need admin privilege to view Funds.")

    @jwt_required()
    @blp.arguments(FundUpdateSchema)
    def post(self, fund_data):
        fund_id = uuid.uuid4().hex
        claim = get_jwt()

        if claim["is_admin"]:

            user = UserModel.query.get_or_404(claim["sub"])

            fund = FundModel(
                id=fund_id,
                fund_type=fund_data["fund_type"].lower(),
                total_fund=fund_data["total_fund"],
                last_updated=datetime.datetime.now(),
                updated_by=f"{user.firstname} {user.lastname}",
                remarks=fund_data["remarks"]
            )
            try:
                db.session.add(fund)
                db.session.commit()
            except IntegrityError:
                abort(400, message=f"Fund information already exist.")
            except SQLAlchemyError as e:
                abort(500, message=f"Encountered an error while adding the user to the database.")

            return {"message": "Fund added successfully."}, 201
