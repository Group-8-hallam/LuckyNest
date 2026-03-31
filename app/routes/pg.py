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

@pg_bp.route('/dashboard')
@login_required
def dashboard():
    payment_data = {
        'montly_rent': 600,
        'room': 'single room 204',
        'next_due': '20 march 2026',
        'ammount_due': 600,
        'history': [
            {'date': '15feb', 'description': 'montly rent', 'ammount': 600, 'status': 'paid'},
            {'date': '05feb', 'description': 'Laundry Service (3 loads)', 'ammount': 5.70, 'status': 'paid'},
            {'date': '01feb', 'description': 'montly rent', 'ammount': 600, 'status': 'paid'},
        ]
    }

    services = {
        'meal_plan': 'weekly - full day',
        'laundary': '4 of 6 uses this weak',
        'housekeeping': '2 of 4 visits this month'
    }

    return render_template('dashboard.html',
                           payment_data=payment_data,
                           services=services)

@pg_bp.route('/meals')
@login_required
def meals():
    return render_template('meals.html')