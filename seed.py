"""
seed.py — LuckyNest Dummy Data
Run this file once to populate your database with test data.

Usage:
    python seed.py
"""

from app import create_app, db
from app.models.user import User
from app.models.rooms import Room
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.meal_plan import MealPlan
from app.models.service_request import ServiceRequest
from app.models.visitor import Visitor
from app.models.notification import Notification
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta

app = create_app()

with app.app_context():

    # ── Clear existing data ────────────────────────────
    print("Clearing existing data...")
    Notification.query.delete()
    Visitor.query.delete()
    ServiceRequest.query.delete()
    MealPlan.query.delete()
    Payment.query.delete()
    Booking.query.delete()
    Room.query.delete()
    User.query.delete()
    db.session.commit()

    # ── Users ──────────────────────────────────────────
    print("Creating users...")

    owner = User(
        full_name='Admin Owner',
        email='owner@luckynest.com',
        phone='+44 7700 000001',
        password_hash=generate_password_hash('password123'),
        role='owner',
        address='1 Owner Street, London',
        date_of_birth=date(1980, 1, 15),
        id_proof_type='Passport',
        id_proof_number='OWN123456',
        is_active=True
    )

    admin = User(
        full_name='Staff Admin',
        email='admin@luckynest.com',
        phone='+44 7700 000002',
        password_hash=generate_password_hash('password123'),
        role='admin',
        address='2 Admin Road, London',
        date_of_birth=date(1990, 5, 20),
        id_proof_type='Driving License',
        id_proof_number='ADM789012',
        is_active=True
    )

    guests = [
        User(full_name='Ronald Polhos',   email='ronald@email.com',  phone='+44 7700 100001', password_hash=generate_password_hash('password123'), role='pg', address='Room 101, LuckyNest', date_of_birth=date(2000, 3, 10), id_proof_type='Passport',         id_proof_number='RP100001', is_active=True),
        User(full_name='Priya Sharma',    email='priya@email.com',   phone='+44 7700 100002', password_hash=generate_password_hash('password123'), role='pg', address='Room 102, LuckyNest', date_of_birth=date(1999, 7, 22), id_proof_type='Aadhar',           id_proof_number='PS100002', is_active=True),
        User(full_name='James OBrien',    email='james@email.com',   phone='+44 7700 100003', password_hash=generate_password_hash('password123'), role='pg', address='Room 103, LuckyNest', date_of_birth=date(2001, 1, 5),  id_proof_type='Driving License',  id_proof_number='JO100003', is_active=True),
        User(full_name='Aisha Patel',     email='aisha@email.com',   phone='+44 7700 100004', password_hash=generate_password_hash('password123'), role='pg', address='Room 104, LuckyNest', date_of_birth=date(2000, 9, 14), id_proof_type='Passport',         id_proof_number='AP100004', is_active=True),
        User(full_name='Mohammed Ali',    email='mohammed@email.com',phone='+44 7700 100005', password_hash=generate_password_hash('password123'), role='pg', address='Room 105, LuckyNest', date_of_birth=date(1998, 11, 30),id_proof_type='Passport',         id_proof_number='MA100005', is_active=True),
        User(full_name='Chen Wei',        email='chen@email.com',    phone='+44 7700 100006', password_hash=generate_password_hash('password123'), role='pg', address='Room 106, LuckyNest', date_of_birth=date(2002, 4, 18), id_proof_type='Passport',         id_proof_number='CW100006', is_active=True),
        User(full_name='Sofia Mendes',    email='sofia@email.com',   phone='+44 7700 100007', password_hash=generate_password_hash('password123'), role='pg', address='Room 201, LuckyNest', date_of_birth=date(1999, 6, 25), id_proof_type='Driving License',  id_proof_number='SM100007', is_active=True),
        User(full_name='Arjun Kumar',     email='arjun@email.com',   phone='+44 7700 100008', password_hash=generate_password_hash('password123'), role='pg', address='Room 202, LuckyNest', date_of_birth=date(2001, 8, 12), id_proof_type='Aadhar',           id_proof_number='AK100008', is_active=True),
        User(full_name='Fatima Hassan',   email='fatima@email.com',  phone='+44 7700 100009', password_hash=generate_password_hash('password123'), role='pg', address='Room 203, LuckyNest', date_of_birth=date(2000, 2, 28), id_proof_type='Passport',         id_proof_number='FH100009', is_active=True),
        User(full_name='Lucas Silva',     email='lucas@email.com',   phone='+44 7700 100010', password_hash=generate_password_hash('password123'), role='pg', address='Room 204, LuckyNest', date_of_birth=date(1997, 12, 3), id_proof_type='Driving License',  id_proof_number='LS100010', is_active=True),
    ]

    db.session.add(owner)
    db.session.add(admin)
    for g in guests:
        db.session.add(g)
    db.session.commit()
    print(f"  Created {len(guests) + 2} users")

    # ── Rooms ──────────────────────────────────────────
    print("Creating rooms...")

    rooms_data = [
        # Ground Floor
        ('101', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('102', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('103', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('104', 1, 'Double', 110.0, 440.0,  200.0, 'WiFi, Desk, Wardrobe, Bathroom',True),
        ('105', 1, 'Double', 110.0, 440.0,  200.0, 'WiFi, Desk, Wardrobe, Bathroom',True),
        ('106', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('107', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          False),
        ('108', 1, 'Triple', 150.0, 600.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',     False),
        ('109', 1, 'Triple', 150.0, 600.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',     False),
        ('110', 1, 'Single', 70.0,  280.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        # Floor 2
        ('201', 2, 'Single', 75.0,  300.0,  150.0, 'WiFi, Desk, Wardrobe, View',    True),
        ('202', 2, 'Single', 75.0,  300.0,  150.0, 'WiFi, Desk, Wardrobe, View',    True),
        ('203', 2, 'Double', 115.0, 460.0,  200.0, 'WiFi, Desk, Bathroom, View',    True),
        ('204', 2, 'Double', 115.0, 460.0,  200.0, 'WiFi, Desk, Bathroom, View',    True),
        ('205', 2, 'Single', 75.0,  300.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('206', 2, 'Single', 75.0,  300.0,  150.0, 'WiFi, Desk, Wardrobe',          False),
        ('207', 2, 'Triple', 155.0, 620.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',     True),
        ('208', 2, 'Triple', 155.0, 620.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',     True),
        ('209', 2, 'Single', 75.0,  300.0,  150.0, 'WiFi, Desk, Wardrobe',          False),
        ('210', 2, 'Double', 115.0, 460.0,  200.0, 'WiFi, Desk, Bathroom',          True),
        # Floor 3
        ('301', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe, View',    True),
        ('302', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe, View',    True),
        ('303', 3, 'Double', 120.0, 480.0,  200.0, 'WiFi, Desk, Bathroom, View',    True),
        ('304', 3, 'Double', 120.0, 480.0,  200.0, 'WiFi, Desk, Bathroom, View',    True),
        ('305', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('306', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('307', 3, 'Triple', 160.0, 640.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',     False),
        ('308', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        ('309', 3, 'Double', 120.0, 480.0,  200.0, 'WiFi, Desk, Bathroom',          True),
        ('310', 3, 'Single', 80.0,  320.0,  150.0, 'WiFi, Desk, Wardrobe',          True),
        # Floor 4
        ('401', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe, Rooftop View', True),
        ('402', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe, Rooftop View', True),
        ('403', 4, 'Double', 125.0, 500.0,  200.0, 'WiFi, Desk, Bathroom, Rooftop View', True),
        ('404', 4, 'Double', 125.0, 500.0,  200.0, 'WiFi, Desk, Bathroom, Rooftop View', True),
        ('405', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe',               True),
        ('406', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe',               True),
        ('407', 4, 'Triple', 165.0, 660.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',          True),
        ('408', 4, 'Triple', 165.0, 660.0,  300.0, 'WiFi, 3 Beds, 2 Bathrooms',          True),
        ('409', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe',               False),
        ('410', 4, 'Single', 85.0,  340.0,  150.0, 'WiFi, Desk, Wardrobe, Rooftop View', True),
    ]

    rooms = []
    for r in rooms_data:
        room = Room(
            number=r[0], floor=r[1], type=r[2],
            price_weekly=r[3], price_monthly=r[4],
            security_deposit=r[5], amenities=r[6], is_occupied=r[7]
        )
        db.session.add(room)
        rooms.append(room)
    db.session.commit()
    print(f"  Created {len(rooms)} rooms")

    # ── Bookings ───────────────────────────────────────
    print("Creating bookings...")

    all_users = User.query.filter_by(role='pg').all()
    all_rooms = Room.query.filter_by(is_occupied=True).all()

    bookings = []
    for i, guest in enumerate(all_users[:8]):
        if i < len(all_rooms):
            b = Booking(
                user_id=guest.id,
                room_id=all_rooms[i].id,
                check_in_date=date(2025, 9, 1) + timedelta(days=i * 10),
                check_out_date=None,
                payment_cycle='monthly',
                status='active',
                security_deposit=all_rooms[i].security_deposit,
                total_amount=all_rooms[i].price_monthly,
                notes='Dummy booking'
            )
            db.session.add(b)
            bookings.append(b)
    db.session.commit()
    print(f"  Created {len(bookings)} bookings")

    # ── Payments ───────────────────────────────────────
    print("Creating payments...")

    payment_count = 0
    for i, booking in enumerate(bookings):
        statuses = [True, True, True, False] if i % 3 != 2 else [True, True, False, False]
        for month in range(4):
            due = date(2025, 10, 1) + timedelta(days=month * 30)
            p = Payment(
                booking_id=booking.id,
                amount=booking.total_amount,
                method='bank_transfer',
                status=statuses[month],
                due_date=due,
                payment_date=datetime(2025, 10, 1) + timedelta(days=month * 30) if statuses[month] else None,
                invoice_ref=f'INV-{booking.id}-{month + 1:02d}',
                late_fee_applied=0.0
            )
            db.session.add(p)
            payment_count += 1
    db.session.commit()
    print(f"  Created {payment_count} payments")

    # ── Meal Plans ─────────────────────────────────────
    print("Creating meal plans...")

    plan_types = ['daily', 'weekly', 'monthly']
    meal_types = ['breakfast', 'lunch', 'dinner', 'all']
    meal_count = 0

    for i, guest in enumerate(all_users):
        mp = MealPlan(
            user_id=guest.id,
            plan_type=plan_types[i % 3],
            meal_type=meal_types[i % 4],
            start_date=date(2025, 9, 1),
            end_date=None,
            total_cost=round(30.0 + (i * 5), 2),
            is_active=True
        )
        db.session.add(mp)
        meal_count += 1
    db.session.commit()
    print(f"  Created {meal_count} meal plans")

    # ── Service Requests ───────────────────────────────
    print("Creating service requests...")

    service_types = ['laundry', 'housekeeping', 'maintenance', 'room_service']
    statuses      = ['completed', 'completed', 'pending', 'in_progress']
    sr_count = 0

    for i, guest in enumerate(all_users):
        for j in range(3):
            sr = ServiceRequest(
                user_id=guest.id,
                service_type=service_types[(i + j) % 4],
                details=f'Request for {service_types[(i + j) % 4]} by {guest.full_name}',
                status=statuses[(i + j) % 4],
                requested_at=datetime(2026, 2, 1) + timedelta(days=i + j),
                completed_at=datetime(2026, 2, 3) + timedelta(days=i + j) if statuses[(i + j) % 4] == 'completed' else None,
                cost=round(5.0 + (j * 2.5), 2),
                assigned_admin_id=admin.id
            )
            db.session.add(sr)
            sr_count += 1
    db.session.commit()
    print(f"  Created {sr_count} service requests")

    # ── Visitors ───────────────────────────────────────
    print("Creating visitors...")

    visitor_names    = ['Sarah Johnson', 'Mark Williams', 'Plumber Co.', 'Priya Patel Senior', 'James Brown', 'Delivery Co.', 'Anna Chen']
    visitor_purposes = ['Family', 'Friend', 'Service', 'Family', 'Friend', 'Service', 'Family']
    v_count = 0

    for i, guest in enumerate(all_users[:7]):
        v = Visitor(
            user_id=guest.id,
            visitor_name=visitor_names[i],
            photo_id_type='Driving License',
            id_number=f'VIS{i + 1:04d}',
            purpose=visitor_purposes[i],
            check_in_time=datetime(2026, 2, 10) + timedelta(hours=i * 3),
            check_out_time=datetime(2026, 2, 10) + timedelta(hours=(i * 3) + 2) if i != 4 else None,
            vehicle_number=f'LN{i + 1:02d}ABC' if i % 3 == 0 else None,
            guest_approval=True,
            logged_at=datetime(2026, 2, 10) + timedelta(hours=i * 3)
        )
        db.session.add(v)
        v_count += 1
    db.session.commit()
    print(f"  Created {v_count} visitors")

    # ── Notifications ──────────────────────────────────
    print("Creating notifications...")

    alert_types = ['payment_due', 'visitor_arrived', 'emergency', 'general']
    messages = [
        'Your rent payment is due in 3 days.',
        'A visitor has arrived for you at reception.',
        'Emergency drill scheduled for tomorrow at 10am.',
        'Welcome to LuckyNest! Please complete your profile.'
    ]
    n_count = 0

    for i, guest in enumerate(all_users):
        for j in range(2):
            n = Notification(
                user_id=guest.id,
                alert_type=alert_types[(i + j) % 4],
                message=messages[(i + j) % 4],
                sent_via_email=True,
                sent_via_sms=False,
                sent_via_app=True,
                is_read=j == 0,
                sent_at=datetime(2026, 2, 1) + timedelta(days=i + j),
                created_at=datetime(2026, 2, 1) + timedelta(days=i + j)
            )
            db.session.add(n)
            n_count += 1
    db.session.commit()
    print(f"  Created {n_count} notifications")

    print("\nDone! Database seeded successfully.")
    print(f"\nLogin credentials:")
    print(f"  Owner  — email: owner@luckynest.com  password: password123")
    print(f"  Admin  — email: admin@luckynest.com  password: password123")
    print(f"  Guest  — email: ronald@email.com     password: password123")