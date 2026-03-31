from flask_login import UserMixin
from .. import db

class User(UserMixin, db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    price_weekly = db.Column(db.Float, nullable=False)
    price_monthly = db.Column(db.Float, nullable=False)
    security_deposit = db.Column(db.Float, nullable=True)
    amenities = db.Column(db.String(150), nullable=True)

    is_occupied = db.Column(db.Boolean, default=False)