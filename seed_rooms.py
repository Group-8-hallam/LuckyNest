from app import create_app
from app.models.rooms import Room
from app import db

app = create_app()

with app.app_context():
    # Only seed if no rooms exist
    if Room.query.count() > 0:
        print('Rooms already exist, skipping seed.')
    else:
        rooms = []

        # Ground floor G01-G10
        for i in range(1, 11):
            rooms.append(Room(
                number=f'G{i:02d}',
                floor=0,
                type='single' if i <= 4 else 'double' if i <= 7 else 'triple',
                price_weekly=150 if i <= 4 else 100 if i <= 7 else 70,
                price_monthly=600 if i <= 4 else 400 if i <= 7 else 280,
                security_deposit=750 if i <= 4 else 500 if i <= 7 else 350,
                amenities='WiFi',
                is_occupied=False
            ))

        # Floor 1 - rooms 101-110
        for i in range(1, 11):
            rooms.append(Room(
                number=f'1{i:02d}',
                floor=1,
                type='single' if i <= 4 else 'double' if i <= 7 else 'triple',
                price_weekly=150 if i <= 4 else 100 if i <= 7 else 70,
                price_monthly=600 if i <= 4 else 400 if i <= 7 else 280,
                security_deposit=750 if i <= 4 else 500 if i <= 7 else 350,
                amenities='WiFi',
                is_occupied=False
            ))

        # Floor 2 - rooms 201-210
        for i in range(1, 11):
            rooms.append(Room(
                number=f'2{i:02d}',
                floor=2,
                type='single' if i <= 4 else 'double' if i <= 7 else 'triple',
                price_weekly=150 if i <= 4 else 100 if i <= 7 else 70,
                price_monthly=600 if i <= 4 else 400 if i <= 7 else 280,
                security_deposit=750 if i <= 4 else 500 if i <= 7 else 350,
                amenities='WiFi',
                is_occupied=False
            ))

        # Floor 3 - rooms 301-310
        for i in range(1, 11):
            rooms.append(Room(
                number=f'3{i:02d}',
                floor=3,
                type='single' if i <= 4 else 'double' if i <= 7 else 'triple',
                price_weekly=150 if i <= 4 else 100 if i <= 7 else 70,
                price_monthly=600 if i <= 4 else 400 if i <= 7 else 280,
                security_deposit=750 if i <= 4 else 500 if i <= 7 else 350,
                amenities='WiFi',
                is_occupied=False
            ))

        # Floor 4 - rooms 401-410
        for i in range(1, 11):
            rooms.append(Room(
                number=f'4{i:02d}',
                floor=4,
                type='single' if i <= 4 else 'double' if i <= 7 else 'triple',
                price_weekly=150 if i <= 4 else 100 if i <= 7 else 70,
                price_monthly=600 if i <= 4 else 400 if i <= 7 else 280,
                security_deposit=750 if i <= 4 else 500 if i <= 7 else 350,
                amenities='WiFi',
                is_occupied=False
            ))

        db.session.add_all(rooms)
        db.session.commit()
        print(f'Seeded {len(rooms)} rooms successfully.')