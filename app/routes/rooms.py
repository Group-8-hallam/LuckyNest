from flask import Blueprint, render_template
from ..models.rooms import Room

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/')
def rooms():
    rooms_data = [
        {
            'name': 'Single Room',
            'description': 'Cozy and comfortable, perfect for solo travellers or students.',
            'price_weekly': 150,
            'price_monthly': 600,
            'guests': 1,
            'image': 'single-room.jpg'
        },
        {
            'name': 'Double Room',
            'description': 'Share a room with a flatmate.',
            'price_weekly': 100,
            'price_monthly': 400,
            'guests': 2,
            'image': 'double-room.jpg'
        },
        {
            'name': 'Triple Room',
            'description': 'Share a room with 2 other people.',
            'price_weekly': 70,
            'price_monthly': 280,
            'guests': 3,
            'image': 'triple-room.jpg'
        }
    ]
    return render_template('rooms.html', rooms=rooms_data)