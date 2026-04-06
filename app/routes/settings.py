from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .. import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.dob = request.form.get('dob')

        db.session.commit()
        return redirect(url_for('settings.settings'))

    return render_template('settings.html', user=current_user)