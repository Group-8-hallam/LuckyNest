from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/reports')
def reports():
    return render_template('reports.html')

@main_bp.route('/occupancy')
def reports():
    return render_template('occupancy.html')

@main_bp.route('/food_report')
def reports():
    return render_template('food_report.html')