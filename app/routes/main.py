from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/reports')
def reports():
    return render_template('reports.html')

@main_bp.route('/occupancy')
def occupancy():
    return render_template('occupancy.html')

@main_bp.route('/food-report')
def food_report():
    return render_template('food_report.html')

@main_bp.route('/guest-report')
def guest_report():
    return render_template('guest_report.html')

@main_bp.route('/service-report')
def service_report():
    return render_template('service_report.html')

@main_bp.route('/visitor-report')
def visitor_report():
    return render_template('visitor_report.html')

@main_bp.route('/guest/all')
def guest_all():
    return render_template('guest/all.html')

@main_bp.route('/guest/active')
def guest_active():
    return render_template('guest/active.html')

@main_bp.route('/guest/checkins')
def guest_checkins():
    return render_template('guest/checkins.html')

@main_bp.route('/guest/emergency')
def guest_emergency():
    return render_template('guest/emergency.html')