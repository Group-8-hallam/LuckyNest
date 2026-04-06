from datetime import datetime
from .. import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=True)
    payment_cycle = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    security_deposit = db.Column(db.Float, nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payments = db.relationship('Payment', backref='booking', lazy=True)

    def __repr__(self):
        return f'<Booking {self.id} User:{self.user_id} Room:{self.room_id}>'