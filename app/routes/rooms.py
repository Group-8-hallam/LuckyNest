from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..models.rooms import Room
from .. import db
from functools import wraps

rooms_bp = Blueprint('rooms', __name__)


def owner_or_admin_required(f):
    # Only owners and admins can manage rooms
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['owner', 'admin']:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('pg.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@rooms_bp.route('/')
@login_required
@owner_or_admin_required
def rooms():
    # Pull all rooms from the database, ordered by room number
    all_rooms = Room.query.order_by(Room.number).all()
    return render_template('rooms/rooms.html', rooms=all_rooms)


@rooms_bp.route('/add', methods=['GET', 'POST'])
@login_required
@owner_or_admin_required
def add_room():
    if request.method == 'POST':
        number = request.form.get('number')
        floor = request.form.get('floor')
        room_type = request.form.get('type')
        price_weekly = request.form.get('price_weekly')
        price_monthly = request.form.get('price_monthly')
        security_deposit = request.form.get('security_deposit')
        amenities = request.form.get('amenities')

        # Check room number isn't already taken
        if Room.query.filter_by(number=number).first():
            flash('A room with that number already exists.', 'error')
            return redirect(url_for('rooms.add_room'))

        new_room = Room(
            number=number,
            floor=int(floor) if floor else None,
            type=room_type,
            price_weekly=float(price_weekly),
            price_monthly=float(price_monthly),
            security_deposit=float(security_deposit) if security_deposit else None,
            amenities=amenities,
            is_occupied=False
        )

        db.session.add(new_room)
        db.session.commit()
        flash(f'Room {number} added successfully.', 'success')
        return redirect(url_for('rooms.rooms'))

    return render_template('rooms/add_room.html')


@rooms_bp.route('/edit/<int:room_id>', methods=['GET', 'POST'])
@login_required
@owner_or_admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)

    if request.method == 'POST':
        room.number = request.form.get('number')
        room.floor = request.form.get('floor')
        room.type = request.form.get('type')
        room.price_weekly = float(request.form.get('price_weekly'))
        room.price_monthly = float(request.form.get('price_monthly'))
        room.security_deposit = float(request.form.get('security_deposit')) if request.form.get('security_deposit') else None
        room.amenities = request.form.get('amenities')

        db.session.commit()
        flash(f'Room {room.number} updated successfully.', 'success')
        return redirect(url_for('rooms.rooms'))

    return render_template('rooms/edit_room.html', room=room)


@rooms_bp.route('/toggle/<int:room_id>', methods=['POST'])
@login_required
@owner_or_admin_required
def toggle_room(room_id):
    room = Room.query.get_or_404(room_id)
    room.is_occupied = not room.is_occupied
    db.session.commit()
    status = 'occupied' if room.is_occupied else 'vacant'
    flash(f'Room {room.number} marked as {status}.', 'success')
    return redirect(url_for('rooms.rooms'))


@rooms_bp.route('/delete/<int:room_id>', methods=['POST'])
@login_required
@owner_or_admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    flash(f'Room {room.number} deleted.', 'success')
    return redirect(url_for('rooms.rooms'))