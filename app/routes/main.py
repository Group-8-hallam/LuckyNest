from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User
from app.models.booking import Booking
from app.models.rooms import Room
from app.models.payment import Payment

main_bp = Blueprint('main', __name__)


def build_guest_list():
    bookings = Booking.query.all()
    guests = []

    for booking in bookings:
        user = User.query.get(booking.user_id)

        if user:
            guests.append({
                "id": user.id,
                "name": user.full_name,
                "phone": user.phone,
                "email": user.email,
                "room": booking.room_id,
                "status": booking.status,
                "checkin": booking.check_in_date,
                "emergency_contact": "-"
            })

    return guests


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/amenities')
def amenities():
    return render_template('amenities.html')


@main_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message. We will be in touch shortly.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')


@main_bp.route('/financial-report')
def reports():
    return render_template('reports.html')


@main_bp.route('/occupancy-report')
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
    guests = build_guest_list()

    total_guests = len(guests)
    active_guests = len([g for g in guests if g["status"] == "active"])
    checked_out = len([g for g in guests if g["status"] == "checked_out"])
    emergency_contacts = len([g for g in guests if g["emergency_contact"] != "-"])

    return render_template(
        'guest/all.html',
        guests=guests,
        total_guests=total_guests,
        active_guests=active_guests,
        checked_out=checked_out,
        emergency_contacts=emergency_contacts
    )


@main_bp.route('/guest/add', methods=['POST'])
def add_guest():
    name = request.form.get('name')
    room_id = request.form.get('room_id')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if not name or not room_id:
        return "Name and Room ID are required", 400

    try:
        room_id = int(room_id)
    except ValueError:
        return "Invalid Room ID", 400

    room = Room.query.get(room_id)

    if not room:
        return "Room does not exist", 400

    if room.is_occupied:
        return "Room already occupied", 400

    user = User(
        full_name=name,
        phone=phone,
        email=email,
        password_hash='password123',
        role='pg'
    )
    db.session.add(user)
    db.session.commit()

    booking = Booking(
        user_id=user.id,
        room_id=room_id,
        check_in_date=db.func.current_date(),
        check_out_date=None,
        payment_cycle='monthly',
        status='active',
        security_deposit=room.security_deposit,
        total_amount=room.price_monthly,
        notes='Added from Guest Management'
    )
    db.session.add(booking)

    room.is_occupied = True

    db.session.commit()

    return redirect(url_for('main.guest_all'))


@main_bp.route('/guest/edit/<int:user_id>', methods=['POST'])
def edit_guest(user_id):
    user = User.query.get_or_404(user_id)
    booking = Booking.query.filter_by(user_id=user.id).first()

    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    status = request.form.get('status')

    if name:
        user.full_name = name
    if phone:
        user.phone = phone
    if email:
        user.email = email
    if booking and status:
        booking.status = status

        if status == 'checked_out':
            booking.check_out_date = db.func.current_date()
            room = Room.query.get(booking.room_id)
            if room:
                room.is_occupied = False
        elif status == 'active':
            booking.check_out_date = None
            room = Room.query.get(booking.room_id)
            if room:
                room.is_occupied = True

    db.session.commit()

    return redirect(url_for('main.guest_all'))


@main_bp.route('/guest/delete/<int:user_id>', methods=['POST'])
def delete_guest(user_id):
    user = User.query.get_or_404(user_id)
    booking = Booking.query.filter_by(user_id=user.id).first()

    if booking:
        payments = Payment.query.filter_by(booking_id=booking.id).all()
        for payment in payments:
            db.session.delete(payment)

        room = Room.query.get(booking.room_id)
        if room:
            room.is_occupied = False

        db.session.delete(booking)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.guest_all'))


@main_bp.route('/guest/toggle-status/<int:user_id>', methods=['POST'])
def toggle_guest_status(user_id):
    user = User.query.get_or_404(user_id)
    booking = Booking.query.filter_by(user_id=user.id).first_or_404()

    if booking.status == 'active':
        booking.status = 'checked_out'
        booking.check_out_date = db.func.current_date()

        room = Room.query.get(booking.room_id)
        if room:
            room.is_occupied = False
    else:
        booking.status = 'active'
        booking.check_out_date = None

        room = Room.query.get(booking.room_id)
        if room:
            room.is_occupied = True

    db.session.commit()

    return redirect(url_for('main.guest_checkins'))


@main_bp.route('/guest/active')
def guest_active():
    guests = build_guest_list()
    return render_template('guest/active.html', guests=guests)


@main_bp.route('/guest/checkins')
def guest_checkins():
    guests = build_guest_list()
    return render_template('guest/checkins.html', guests=guests)


@main_bp.route('/guest/emergency')
def guest_emergency():
    guests = build_guest_list()
    return render_template('guest/emergency.html', guests=guests)


@main_bp.route('/booking')
def booking():
    return render_template('booking.html')