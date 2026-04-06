from datetime import datetime
from .. import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=False)
    late_fee_applied = db.Column(db.Float, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    invoice_ref = db.Column(db.String(100), nullable=True)
    grace_period_end = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.id} Booking:{self.booking_id} Amount:{self.amount}>'