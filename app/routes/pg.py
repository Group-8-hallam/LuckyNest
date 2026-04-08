from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort

pg_bp = Blueprint('pg', __name__)

def pg_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['pg', 'owner', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@pg_bp.route('/meals')
@login_required
def meals():
    return render_template('meals.html')

@pg_bp.route('/payment')
@login_required
def payment():
    price = request.args.get('price')
    plan = request.args.get('plan')
    return render_template('payment.html', price=price, plan=plan)

from app.models.rooms import Room

@pg_bp.route('/dashboard')
@login_required
def dashboard():

    # ── Room stats ─────────────────────────────
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(is_occupied=True).count()

    # ── Payment data ───────────────────────────
    payment_data = {
        'monthly_rent': 600,
        'room': 'single room 204',
        'next_due': '20 March 2026',
        'amount_due': 600,
        'history': [
            {'date': '15 Feb', 'description': 'monthly rent', 'amount': 600, 'status': 'paid'},
            {'date': '05 Feb', 'description': 'Laundry Service (3 loads)', 'amount': 5.70, 'status': 'paid'},
            {'date': '01 Feb', 'description': 'monthly rent', 'amount': 600, 'status': 'paid'},
        ]
    }

    # ── Services data ──────────────────────────
    services = {
        'meal_plan': 'weekly - full day',
        'laundry': '4 of 6 uses this week',
        'housekeeping': '2 of 4 visits this month'
    }

    return render_template(
        'dashboard.html',
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        payment_data=payment_data,
        services=services
    )

from flask import request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import db
from datetime import datetime

@pg_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    if request.method == 'POST':

        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')

        dob = request.form.get('date_of_birth')
        if dob:
            current_user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()

        db.session.commit()
        flash("Profile updated successfully!", "success")

        return redirect(url_for('pg.settings'))

    return render_template('settings.html', user=current_user)