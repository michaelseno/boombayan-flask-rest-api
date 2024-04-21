from db import db
import datetime


class FundModel(db.Model):
    __tablename__ = "funds"

    id = db.Column(db.String(), primary_key=True)
    fund_type = db.Column(db.String(), nullable=False, unique=True)
    total_fund = db.Column(db.Float(), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String(), nullable=False)
    remarks = db.Column(db.String(), nullable=False)



