from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.notification import Notification
from ..models.user import User
from .. import db
from functools import wraps

owner_bp = Blueprint('owner', __name__)

def owner_required(f):
    # Blocks anyone who isn't an owner from accessing these pages
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'owner':
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('pg.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@owner_bp.route('/send-notification', methods=['GET', 'POST'])
@login_required
@owner_required
def send_notification():
    # Get all PG users to populate the dropdown
    pg_users = User.query.filter_by(role='pg').all()

    if request.method == 'POST':
        recipient = request.form.get('recipient')  # 'all' or a user id
        alert_type = request.form.get('alert_type')
        message = request.form.get('message')

        if recipient == 'all':
            # Send to every PG
            for user in pg_users:
                notification = Notification(
                    user_id=user.id,
                    alert_type=alert_type,
                    message=message,
                    sent_via_app=True
                )
                db.session.add(notification)
        else:
            # Send to one specific PG
            notification = Notification(
                user_id=int(recipient),
                alert_type=alert_type,
                message=message,
                sent_via_app=True
            )
            db.session.add(notification)

        db.session.commit()
        flash('Notification sent successfully.', 'success')
        return redirect(url_for('owner.send_notification'))

    return render_template('owner/send_notification.html',
                           pg_users=pg_users)