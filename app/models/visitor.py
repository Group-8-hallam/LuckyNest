from datetime import datetime
from .. import db

class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visitor_name = db.Column(db.String(100), nullable=False)
    photo_id_type = db.Column(db.String(50), nullable=True)
    id_number = db.Column(db.String(100), nullable=True)
    purpose = db.Column(db.String(100), nullable=True)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)
    vehicle_number = db.Column(db.String(50), nullable=True)
    guest_approval = db.Column(db.Boolean, default=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Visitor {self.visitor_name} User:{self.user_id}>'