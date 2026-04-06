from datetime import datetime
from .. import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_via_email = db.Column(db.Boolean, default=False)
    sent_via_sms = db.Column(db.Boolean, default=False)
    sent_via_app = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.id} User:{self.user_id} Type:{self.alert_type}>'