from db import db


class LoanModel(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), nullable=False)
    loan_amount = db.Column(db.Float(), nullable=False)
    payment_term = db.Column(db.Integer(), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False)
    first_approve = db.Column(db.String())
    date_first_approved = db.Column(db.DateTime)
    second_approve = db.Column(db.String())
    date_second_approved = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean, nullable=False)
