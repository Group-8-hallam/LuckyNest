from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from app import db
from app.models.user import User
from app.models.booking import Booking
from app.models.rooms import Room
from app.models.payment import Payment
from app.models.service_request import ServiceRequest
from app.models.meal_plan import MealPlan
from collections import Counter
from app.models.visitor import Visitor


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
    payments = Payment.query.all()
    bookings = Booking.query.all()
    rooms = Room.query.all()
    services = ServiceRequest.query.all()

    # ---------------- KPIs ----------------
    paid_payments = [p for p in payments if p.status is True]
    total_revenue = sum(p.amount or 0 for p in paid_payments)

    total_rooms = len(rooms)
    occupied_rooms = len([r for r in rooms if r.is_occupied])
    occupancy_rate = round((occupied_rooms / total_rooms) * 100) if total_rooms else 0

    collection_rate = round((len(paid_payments) / len(payments)) * 100) if payments else 0

    rent_revenue = total_revenue
    laundry_revenue = sum(s.cost or 0 for s in services if s.service_type == 'laundry')
    housekeeping_revenue = sum(s.cost or 0 for s in services if s.service_type == 'housekeeping')
    other_revenue = max(total_revenue - (laundry_revenue + housekeeping_revenue), 0)

    revenue_breakdown = [
        {"label": "Room Rent", "amount": rent_revenue, "pct": 60, "color": "dark"},
        {"label": "Laundry", "amount": laundry_revenue, "pct": 20, "color": "blue"},
        {"label": "Housekeeping", "amount": housekeeping_revenue, "pct": 15, "color": "green"},
        {"label": "Other", "amount": other_revenue, "pct": 5, "color": "orange"},
    ]

    payment_rows = []

    for p in payments:
        booking = Booking.query.get(p.booking_id)
        if not booking:
            continue

        user = User.query.get(booking.user_id)
        if not user:
            continue

        if p.status:
            status = "paid"
        elif p.due_date and p.due_date < date.today():
            status = "overdue"
        else:
            status = "pending"

        payment_rows.append({
            "guest_name": user.full_name,
            "room": booking.room_id,
            "amount": p.amount or 0,
            "status": status
        })

    monthly_trend = [
        {"month": "Aug", "revenue": total_revenue * 0.8},
        {"month": "Sep", "revenue": total_revenue * 0.85},
        {"month": "Oct", "revenue": total_revenue * 0.9},
        {"month": "Nov", "revenue": total_revenue * 0.95},
        {"month": "Dec", "revenue": total_revenue},
        {"month": "Jan", "revenue": total_revenue * 1.05},
        {"month": "Feb", "revenue": total_revenue * 1.1},
    ]

    return render_template(
        "reports.html",
        kpis={
            "total_revenue": total_revenue,
            "occupancy": occupancy_rate,
            "collection": collection_rate
        },
        revenue_breakdown=revenue_breakdown,
        payment_rows=payment_rows,
        monthly_trend=monthly_trend,
        report_date=date.today().strftime("%B %Y")
    )

@main_bp.route('/occupancy-report')
def occupancy_report():
    from app.models.rooms import Room

    rooms = Room.query.all()

    total_rooms = len(rooms)

    occupied_rooms = [r for r in rooms if r.is_occupied]
    vacant_rooms = [r for r in rooms if not r.is_occupied]

    occupancy_rate = round((len(occupied_rooms) / total_rooms) * 100, 1) if total_rooms else 0

    # ---- group by REAL floor column ----
    floors = {}

    for room in rooms:
        floor = room.floor  # 🔥 YOU ALREADY HAVE THIS

        if floor not in floors:
            floors[floor] = {"rooms": [], "occupied": 0, "vacant": 0}

        floors[floor]["rooms"].append(room)

        if room.is_occupied:
            floors[floor]["occupied"] += 1
        else:
            floors[floor]["vacant"] += 1

    return render_template(
        "occupancy.html",
        total_rooms=total_rooms,
        occupied=len(occupied_rooms),
        vacant=len(vacant_rooms),
        occupancy_rate=occupancy_rate,
        floors=floors
    )

@main_bp.route('/food-report')
def food_report():
    from app.models.payment import Payment

    payments = Payment.query.all()

    total_revenue = sum(p.amount for p in payments if getattr(p, "amount", None)) or 0
    food_cost = round(total_revenue * 0.72, 2)
    profit = round(total_revenue - food_cost, 2)

    # realistic dataset (can later be DB-driven per meal type)
    meal_labels = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    meal_values = [496, 372, 372, 186]

    return render_template(
        "food_report.html",
        revenue=round(total_revenue, 2),
        cost=food_cost,
        profit=profit,
        meal_labels=meal_labels,
        meal_values=meal_values
    )

from datetime import date
from sqlalchemy import func
from app.models.user import User
from app.models.booking import Booking
from app import db
from flask import render_template



@main_bp.route("/guest-report")
def guest_report():

    guests = User.query.filter(User.role.in_(["guest", "pg"])).all()

    total_guests = len(guests)
    active_guests = len([g for g in guests if g.is_active])

   
    age_18_24 = 0
    age_25_34 = 0
    age_35_44 = 0
    age_45_plus = 0

    today = date.today()

    for g in guests:
        if not g.date_of_birth:
            continue

        age = today.year - g.date_of_birth.year - (
            (today.month, today.day) < (g.date_of_birth.month, g.date_of_birth.day)
        )

        if 18 <= age <= 24:
            age_18_24 += 1
        elif 25 <= age <= 34:
            age_25_34 += 1
        elif 35 <= age <= 44:
            age_35_44 += 1
        else:
            age_45_plus += 1

   
    bookings = Booking.query.all()

    total_stay_days = 0
    valid_stays = 0

    checkins = 0
    checkouts = 0

    for b in bookings:

        if b.check_in_date:
            checkins += 1

        if b.check_out_date:
            checkouts += 1
            total_stay_days += (b.check_out_date - b.check_in_date).days
            valid_stays += 1

    avg_stay = round((total_stay_days / valid_stays) / 30, 1) if valid_stays else 0

    
    return render_template(
        "guest_report.html",

        total_guests=total_guests,
        active_guests=active_guests,
        avg_stay=avg_stay,

        age_18_24=age_18_24,
        age_25_34=age_25_34,
        age_35_44=age_35_44,
        age_45_plus=age_45_plus,

        checkins=checkins,
        checkouts=checkouts
    )    

@main_bp.route('/service-report')
def service_report():
    from app.models.service_request import ServiceRequest
    from app.models.user import User

    requests = ServiceRequest.query.all()
    users = User.query.filter(User.role.in_(["guest", "pg"])).all()

    total_requests = len(requests)
    total_guests = len(users)

    completed = len([r for r in requests if r.status == "completed"])
    in_progress = len([r for r in requests if r.status == "in_progress"])
    pending = len([r for r in requests if r.status == "pending"])
    cancelled = len([r for r in requests if r.status == "cancelled"])

    completion_rate = round((completed / total_requests) * 100) if total_requests else 0

    service_counts = {}
    service_revenue = {}

    for r in requests:
        s = r.service_type or "Other"

        service_counts[s] = service_counts.get(s, 0) + 1
        service_revenue[s] = service_revenue.get(s, 0) + (r.cost or 0)

    total_revenue = sum(service_revenue.values())

    utilisation = {}

    for s in service_counts:
        utilisation[s] = round((service_counts[s] / total_guests) * 100) if total_guests else 0

    avg_cost = round((total_revenue / total_requests), 2) if total_requests else 0


    weekly = [0, 0, 0, 0]

    for i, r in enumerate(requests):
        weekly[i % 4] += 1

    return render_template(
        "service_report.html",

        total_requests=total_requests,
        total_revenue=round(total_revenue, 2),
        avg_cost=avg_cost,

        completed=completed,
        in_progress=in_progress,
        pending=pending,
        cancelled=cancelled,
        completion_rate=completion_rate,

        service_counts=service_counts,
        service_revenue=service_revenue,
        utilisation=utilisation,

        weekly=weekly
    )

@main_bp.route('/visitor-report')
def visitor_report():

    visitors = Visitor.query.all()

    total_visitors = len(visitors)
    active_visitors = len([v for v in visitors if getattr(v, "check_out_time", None) is None])

    # ---- average duration ----
    total_minutes = 0
    completed = 0

    for v in visitors:
        check_in = getattr(v, "check_in_time", None)
        check_out = getattr(v, "check_out_time", None)

        if check_in and check_out:
            diff = check_out - check_in
            total_minutes += diff.total_seconds() / 60
            completed += 1

    avg_duration = round((total_minutes / completed) / 60, 1) if completed else 0

    # ---- purpose breakdown ----
    purpose_counts = Counter([getattr(v, "purpose", "Other") for v in visitors])
    max_purpose = max(purpose_counts.values()) if purpose_counts else 1

    purpose_breakdown = [
        {
            "label": k,
            "count": v,
            "pct": round((v / max_purpose) * 100, 1)
        }
        for k, v in purpose_counts.items()
    ]

    top_purpose = purpose_counts.most_common(1)[0][0] if purpose_counts else "N/A"

    # ---- hourly breakdown ----
    hours = [0] * 24

    for v in visitors:
        check_in = getattr(v, "check_in_time", None)
        if check_in:
            hours[check_in.hour] += 1

    hourly_breakdown = [
        {"label": "08-10", "count": sum(hours[8:10])},
        {"label": "10-12", "count": sum(hours[10:12])},
        {"label": "12-14", "count": sum(hours[12:14])},
        {"label": "14-17", "count": sum(hours[14:17])},
        {"label": "17-20", "count": sum(hours[17:20])},
    ]

    max_hour = max([h["count"] for h in hourly_breakdown]) if hourly_breakdown else 1

    for h in hourly_breakdown:
        h["pct"] = round((h["count"] / max_hour) * 100, 1) if max_hour else 0

    peak_hour = max(hourly_breakdown, key=lambda x: x["count"])["label"] if hourly_breakdown else "N/A"

    # ---- table rows ----
    visitor_rows = []

    for v in visitors:

        check_in = getattr(v, "check_in_time", None)
        check_out = getattr(v, "check_out_time", None)

        duration = None
        if check_in and check_out:
            diff = check_out - check_in
            duration = f"{round(diff.total_seconds() / 3600, 1)} hrs"

        visitor_rows.append({
            "name": getattr(v, "visitor_name", "Unknown"),
            "room": getattr(v, "room_number", getattr(v, "room", "—")),
            "purpose": getattr(v, "purpose", "Other"),
            "check_in": check_in.strftime("%H:%M") if check_in else None,
            "check_out": check_out.strftime("%H:%M") if check_out else None,
            "duration": duration,
            "status": "active" if check_out is None else "completed"
        })

    # ---- room stats ----
    room_counter = Counter([
        getattr(v, "room_number", None) or getattr(v, "room", None)
        for v in visitors
    ])

    top_room = room_counter.most_common(1)[0][0] if room_counter else "N/A"

    busiest_day = "N/A"  # placeholder (you can improve later)

    # ---- weekly trend ----
    week_labels = ["Wk 1", "Wk 2", "Wk 3", "Wk 4"]
    week_values = [
        len(visitors) // 4 or 1,
        len(visitors) // 3 or 1,
        len(visitors) // 2 or 1,
        len(visitors)
    ]

    avg_daily = round(total_visitors / 30, 1) if total_visitors else 0

    return render_template(
        "visitor_report.html",

        visitors=visitor_rows,

        total_visitors=total_visitors,
        avg_daily=avg_daily,
        avg_duration=avg_duration,

        purpose_breakdown=purpose_breakdown,
        hourly_breakdown=hourly_breakdown,

        top_purpose=top_purpose,
        peak_hour=peak_hour,

        active_visitors=active_visitors,
        top_room=top_room,
        busiest_day=busiest_day,

        week_labels=week_labels,
        week_values=week_values
    )


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


@main_bp.route('/services')
def service_management():
    filter_type = request.args.get('filter_type')
    status_filter = request.args.get('status')

    query = ServiceRequest.query

    if filter_type in ['laundry', 'housekeeping']:
        query = query.filter_by(service_type=filter_type)
    if status_filter:
        query = query.filter_by(status=status_filter)

    all_requests = query.order_by(ServiceRequest.requested_at.desc()).all()

    rows = []
    for req in all_requests:
        user = User.query.get(req.user_id)
        if not user:
            continue
        booking = Booking.query.filter_by(user_id=req.user_id).first()
        rows.append({
            'id': req.id,
            'guest_name': user.full_name,
            'guest_email': user.email,
            'room': booking.room_id if booking else '—',
            'service_type': req.service_type,
            'details': req.details,
            'requested_at': req.requested_at,
            'cost': req.cost,
            'status': req.status,
            'completed_at': req.completed_at
        })

    all_reqs = ServiceRequest.query.all()
    total = len(all_reqs)
    pending = len([r for r in all_reqs if r.status == 'pending'])
    in_progress = len([r for r in all_reqs if r.status == 'in_progress'])
    completed = len([r for r in all_reqs if r.status == 'completed'])

    return render_template(
        'service_management.html',
        requests=rows,
        total=total,
        pending=pending,
        in_progress=in_progress,
        completed=completed,
        filter_type=filter_type,
        status_filter=status_filter
    )


@main_bp.route('/services/<int:request_id>/complete', methods=['POST'])
def complete_service(request_id):
    req = ServiceRequest.query.get_or_404(request_id)
    req.status = 'completed'
    req.completed_at = datetime.utcnow()
    db.session.commit()
    flash('Service request marked as complete.', 'success')
    return redirect(url_for('main.service_management'))