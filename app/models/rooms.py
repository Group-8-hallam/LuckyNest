from .. import db

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    price_weekly = db.Column(db.Float, nullable=False)
    price_monthly = db.Column(db.Float, nullable=False)
    security_deposit = db.Column(db.Float, nullable=True)
    amenities = db.Column(db.String(150), nullable=True)
    is_occupied = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Room {self.number} ({self.type})>'