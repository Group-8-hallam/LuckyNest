from flask import Blueprint, render_template

bp = Blueprint('rooms', __name__)

@bp.route('/rooms')
def rooms():
    rooms_data = [
        {
            'name': 'Single Room',
            'description': 'Cozy and comfortable, perfect for solo travelers or students.',
            'price': 150,
            'bed': '1 Double Bed',
            'guests': 1,
            'image': 'single-room.jpg'
        },
        {
            'name': 'Double Room',
            'description': 'Share a room with a room mate.',
            'price': 100,
            'bed': '1 Double Bed',
            'guests': 2,
            'image': 'double-room.jpg'
        },
        {
            'name': 'Triple Room',
            'description': 'Share a room with 2 other people',
            'price': 70,
            'bed': '1 Double Bed',
            'guests': 3,
            'image': 'triple-room.jpg'
        }
    ]
    return render_template('rooms.html', rooms=rooms_data)