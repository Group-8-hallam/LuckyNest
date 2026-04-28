from app import create_app, db
from app.models.user import User
from app.models.rooms import Room
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Owner account
    if not User.query.filter_by(email='owner@luckynest.com').first():
        owner = User(
            full_name='Ms Lucky',
            email='owner@luckynest.com',
            phone='07000000000',
            password_hash=generate_password_hash('owner1234'),
            role='owner'
        )
        db.session.add(owner)
        print('Owner account created: owner@luckynest.com / owner1234')
    else:
        print('Owner already exists, skipping.')

    # Seed 50 rooms if none exist
    if Room.query.count() == 0:
        rooms = []
        floors = {
            0: ('G', range(1, 11)),
            1: ('1', range(1, 11)),
            2: ('2', range(1, 11)),
            3: ('3', range(1, 11)),
            4: ('4', range(1, 11)),
        }
        for floor, (prefix, nums) in floors.items():
            for i in nums:
                room_type = 'single' if i <= 4 else 'double' if i <= 7 else 'triple'
                rooms.append(Room(
                    number=f'{prefix}{i:02d}',
                    floor=floor,
                    type=room_type,
                    price_weekly=150 if room_type == 'single' else 100 if room_type == 'double' else 70,
                    price_monthly=600 if room_type == 'single' else 400 if room_type == 'double' else 280,
                    security_deposit=750 if room_type == 'single' else 500 if room_type == 'double' else 350,
                    amenities='WiFi',
                    is_occupied=False
                ))
        db.session.add_all(rooms)
        print(f'Seeded 50 rooms.')
    else:
        print(f'Rooms already exist, skipping.')

    db.session.commit()
    print('Setup complete.')