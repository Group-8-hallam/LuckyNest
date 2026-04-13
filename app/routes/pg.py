from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.rooms import Room
from app.models.booking import Booking
from app.models.payment import Payment
from datetime import datetime, date
from ..models.notification import Notification

pg_bp = Blueprint('pg', __name__)


def pg_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['pg', 'owner', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def build_pg_payment_history(user_id):
    booking = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).first()
    payment_rows = []

    if not booking:
        return None, payment_rows

    payments = Payment.query.filter_by(booking_id=booking.id).order_by(Payment.created_at.desc()).all()

    for payment in payments:
        if payment.status is True:
            status_text = 'paid'
        else:
            if payment.due_date and payment.due_date < date.today():
                status_text = 'overdue'
            else:
                status_text = 'pending'

        if payment.invoice_ref:
            description = f"Invoice {payment.invoice_ref}"
        else:
            description = f"{booking.payment_cycle.capitalize()} payment" if booking.payment_cycle else "Payment record"

        payment_rows.append({
            "id": payment.id,
            "amount": payment.amount or 0,
            "description": description,
            "date": payment.payment_date.date() if payment.payment_date else payment.created_at.date(),
            "method": payment.method or "Not set",
            "status": status_text,
            "invoice_ref": payment.invoice_ref or f"INV-{payment.id:04d}",
            "due_date": payment.due_date,
            "late_fee_applied": payment.late_fee_applied or 0
        })

    return booking, payment_rows


@pg_bp.route('/meals')
@login_required
def meals():
    return render_template('meals.html')


@pg_bp.route('/payment')
@login_required
def payment():
    booking, payments = build_pg_payment_history(current_user.id)

    paid_count = len([p for p in payments if p["status"] == "paid"])
    pending_count = len([p for p in payments if p["status"] == "pending"])
    overdue_count = len([p for p in payments if p["status"] == "overdue"])
    total_paid = sum(p["amount"] for p in payments if p["status"] == "paid")
    total_due = sum(p["amount"] for p in payments if p["status"] in ["pending", "overdue"])

    next_due = None
    due_payments = [p for p in payments if p["status"] in ["pending", "overdue"] and p["due_date"]]
    if due_payments:
        next_due = sorted(due_payments, key=lambda x: x["due_date"])[0]["due_date"]

    return render_template(
        'payment.html',
        booking=booking,
        payments=payments,
        paid_count=paid_count,
        pending_count=pending_count,
        overdue_count=overdue_count,
        total_paid=total_paid,
        total_due=total_due,
        next_due=next_due
    )


@pg_bp.route('/pay/<int:payment_id>', methods=['POST'])
@login_required
def pay_now(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    booking = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).first()

    if not booking or payment.booking_id != booking.id:
        abort(403)

    payment.status = True
    payment.payment_date = datetime.utcnow()
    payment.late_fee_applied = payment.late_fee_applied or 0.0

    db.session.commit()
    flash('Payment completed successfully!', 'success')
    return redirect(url_for('pg.payment'))


@pg_bp.route('/dashboard')
@login_required
def dashboard():
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(is_occupied=True).count()

    occupancy_rate = round((occupied_rooms / total_rooms) * 100) if total_rooms > 0 else 0

    booking, payments = build_pg_payment_history(current_user.id)

    total_paid = sum(p["amount"] for p in payments if p["status"] == "paid")
    total_due = sum(p["amount"] for p in payments if p["status"] in ["pending", "overdue"])

    next_due = None
    due_payments = [p for p in payments if p["status"] in ["pending", "overdue"] and p["due_date"]]
    if due_payments:
        next_due = sorted(due_payments, key=lambda x: x["due_date"])[0]["due_date"]

    payment_data = {
        'monthly_rent': booking.total_amount if booking and booking.total_amount else 0,
        'room': f"Room {booking.room_id}" if booking else 'Not assigned',
        'next_due': next_due.strftime('%d %B %Y') if next_due else 'No pending due date',
        'amount_due': total_due,
        'history': payments[:3]
    }

    services = {
        'meal_plan': 'weekly - full day',
        'laundry': '4 of 6 uses this week',
        'housekeeping': '2 of 4 visits this month'
    }

    return render_template(
        'dashboard.html',
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        occupancy_rate=occupancy_rate,
        payment_data=payment_data,
        services=services
    )

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

@pg_bp.route('/notifications')
@login_required
def notifications():
    # Get all notifications for the logged in user, newest first
    user_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()

    # Mark all unread ones as read when they visit the page
    unread = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).all()

    for n in unread:
        n.is_read = True
    db.session.commit()

    return render_template('pg/notifications.html',
                           notifications=user_notifications)