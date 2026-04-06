from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Booking, Room
from flask_login import login_required, current_user

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/')
@login_required
def booking_home():
    rooms = Room.query.all()
    return render_template('booking.html', rooms=rooms)


@booking_bp.route('/create', methods=['POST'])
@login_required
def create_booking():
    room_id = request.form.get('room_id')

    new_booking = Booking(
        user_id=current_user.id,
        room_id=room_id
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for('booking.booking_home'))