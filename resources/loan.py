from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import LoanModel, UserModel
from schemas import LoanDisplaySchema, ApplyLoanSchema

import uuid
import datetime

blp = Blueprint("Loan", "loan", __name__, description="Operations on loan")


@blp.route("/loan")
class ManageLoan(MethodView):
    @jwt_required()
    @blp.response(200, LoanDisplaySchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["is_admin"]:
            return LoanModel.query.all()
        else:
            abort(404, message="Need admin privilege to view Loan related information.")

    @jwt_required()
    @blp.arguments(ApplyLoanSchema)
    def post(self, loan_data):
        loan_id = uuid.uuid4().hex
        claim = get_jwt()
        user = UserModel.query.get_or_404(claim["sub"])

        if user:
            loan = LoanModel(
                id=loan_id,
                user_id=user.id,
                loan_amount=loan_data["loan_amount"],
                payment_term=loan_data["payment_term"],
                data_applied=datetime.datetime.now(),
                is_approved=False
            )

            try:
                db.session.add(loan)
                db.session.commit()
            except IntegrityError:
                abort(400, message=f"Loan information already exist.")
            except SQLAlchemyError as e:
                abort(500, message=f"Encountered an error while adding the Loan to the database.")

            return {"message": "Loan applied successfully."}, 201
