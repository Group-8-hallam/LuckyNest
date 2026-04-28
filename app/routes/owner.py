from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.notification import Notification
from ..models.user import User
from .. import db
from functools import wraps
from werkzeug.security import generate_password_hash

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

@owner_bp.route('/create-admin', methods=['GET', 'POST'])
@login_required
@owner_required
def create_admin():
    admins = User.query.filter_by(role='admin').order_by(User.created_at).all()

    if request.method == 'POST':
        next_num = len(admins) + 1
        full_name = f'Admin {next_num}'
        email = f'admin-{next_num}@luckynest.com'
        password = f'admin-{next_num}'
        phone = '00000000000'

        if User.query.filter_by(email=email).first():
            flash(f'{email} already exists.', 'error')
            return redirect(url_for('owner.create_admin'))

        new_admin = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password),
            role='admin'
        )
        db.session.add(new_admin)
        db.session.commit()
        flash(f'Admin account created — {email} / {password}', 'success')
        return redirect(url_for('owner.create_admin'))

    return render_template('owner/create_admin.html', admins=admins)

@owner_bp.route('/delete-admin/<int:user_id>', methods=['POST'])
@login_required
@owner_required
def delete_admin(user_id):
    admin = User.query.get_or_404(user_id)
    
    # Safety check - only delete admin accounts, never owner
    if admin.role != 'admin':
        flash('You can only delete admin accounts.', 'error')
        return redirect(url_for('owner.create_admin'))
    
    db.session.delete(admin)
    db.session.commit()
    flash(f'{admin.email} has been deleted.', 'success')
    return redirect(url_for('owner.create_admin'))