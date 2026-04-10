from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
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
                "checkout": booking.check_out_date,
                "emergency_contact": "-",
                "stay_duration": ((booking.check_out_date or date.today()) - booking.check_in_date).days if booking.check_in_date else 0
            })

    return guests


def build_payment_list(payments):
    payment_rows = []

    for payment in payments:
        booking = Booking.query.get(payment.booking_id)
        if not booking:
            continue

        user = User.query.get(booking.user_id)
        if not user:
            continue

        if payment.status is True:
            status_text = 'paid'
        else:
            if payment.due_date and payment.due_date < date.today():
                status_text = 'overdue'
            else:
                status_text = 'pending'

        payment_rows.append({
            "id": payment.id,
            "guest_name": user.full_name,
            "guest_email": user.email,
            "guest_phone": user.phone,
            "room": booking.room_id,
            "amount": payment.amount or 0,
            "date": payment.payment_date.date() if payment.payment_date else payment.created_at.date(),
            "method": payment.method or "Not set",
            "status": status_text,
            "invoice_ref": payment.invoice_ref or f"INV-{payment.id:04d}",
            "due_date": payment.due_date,
            "late_fee_applied": payment.late_fee_applied or 0,
            "grace_period_end": payment.grace_period_end,
            "booking_total": booking.total_amount or 0,
            "payment_cycle": booking.payment_cycle or "Not set"
        })

    return payment_rows


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
        flash('Name and Room ID are required.', 'error')
        return redirect(url_for('main.guest_all'))

    try:
        room_id = int(room_id)
    except ValueError:
        flash('Invalid Room ID.', 'error')
        return redirect(url_for('main.guest_all'))

    room = Room.query.get(room_id)

    if not room:
        flash('Room does not exist.', 'error')
        return redirect(url_for('main.guest_all'))

    if room.is_occupied:
        flash('Room already occupied.', 'error')
        return redirect(url_for('main.guest_all'))

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

    flash('Guest added successfully.', 'success')
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
    if phone is not None:
        user.phone = phone
    if email is not None:
        user.email = email

    if booking and status:
        booking.status = status

        room = Room.query.get(booking.room_id)

        if status == 'checked_out':
            booking.check_out_date = db.func.current_date()
            if room:
                room.is_occupied = False
        elif status == 'active':
            booking.check_out_date = None
            if room:
                room.is_occupied = True

    db.session.commit()

    flash('Guest details updated successfully.', 'success')
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

    flash('Guest removed successfully.', 'success')
    return redirect(url_for('main.guest_all'))


@main_bp.route('/guest/toggle-status/<int:user_id>', methods=['POST'])
def toggle_guest_status(user_id):
    user = User.query.get_or_404(user_id)
    booking = Booking.query.filter_by(user_id=user.id).first_or_404()

    room = Room.query.get(booking.room_id)

    if booking.status == 'active':
        booking.status = 'checked_out'
        booking.check_out_date = db.func.current_date()
        if room:
            room.is_occupied = False
        flash('Guest checked out successfully.', 'success')
    else:
        booking.status = 'active'
        booking.check_out_date = None
        if room:
            room.is_occupied = True
        flash('Guest marked active successfully.', 'success')

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


@main_bp.route('/payment/transactions')
def payment_transactions():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    payment_rows = build_payment_list(payments)
    return render_template('payment/transactions.html', payments=payment_rows)


@main_bp.route('/payment/invoice/<int:payment_id>')
def payment_invoice_detail(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    booking = Booking.query.get_or_404(payment.booking_id)
    user = User.query.get_or_404(booking.user_id)

    if payment.status is True:
        status_text = 'paid'
    else:
        if payment.due_date and payment.due_date < date.today():
            status_text = 'overdue'
        else:
            status_text = 'pending'

    payment_detail = {
        "id": payment.id,
        "guest_name": user.full_name,
        "guest_email": user.email,
        "guest_phone": user.phone,
        "room": booking.room_id,
        "amount": payment.amount or 0,
        "date": payment.payment_date.date() if payment.payment_date else payment.created_at.date(),
        "method": payment.method or "Not set",
        "status": status_text,
        "invoice_ref": payment.invoice_ref or f"INV-{payment.id:04d}",
        "due_date": payment.due_date,
        "late_fee_applied": payment.late_fee_applied or 0,
        "grace_period_end": payment.grace_period_end,
        "payment_cycle": booking.payment_cycle or "Not set",
        "booking_total": booking.total_amount or 0,
        "checkin": booking.check_in_date,
        "checkout": booking.check_out_date
    }

    return render_template('payment/invoices.html', payment=payment_detail)


@main_bp.route('/payment/pending')
def payment_pending():
    payments = Payment.query.filter_by(status=False).order_by(Payment.created_at.desc()).all()
    payment_rows = build_payment_list(payments)
    return render_template('payment/pending.html', payments=payment_rows)


@main_bp.route('/payment/deposits')
def payment_deposits():
    bookings = Booking.query.filter(Booking.security_deposit.isnot(None)).all()
    deposit_rows = []

    for booking in bookings:
        user = User.query.get(booking.user_id)
        if user:
            deposit_rows.append({
                "booking_id": booking.id,
                "guest_name": user.full_name,
                "guest_email": user.email,
                "room": booking.room_id,
                "deposit_amount": booking.security_deposit or 0,
                "status": booking.status,
                "checkin": booking.check_in_date
            })

    return render_template('payment/deposits.html', deposits=deposit_rows)


@main_bp.route('/booking')
def booking():
    return render_template('booking.html')