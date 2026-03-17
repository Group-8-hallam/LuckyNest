from flask import Blueprint, render_template

bp = Blueprint('amenities', __name__)

@bp.route('/amenities')
def amenities():
    # Amenities data
    amenities_data = [
        {'name': 'Free WiFi', 'description': 'Available for free for all rooms. No setup required.'},
        {'name': 'Laundry Services', 'description': 'Available on request: £1.90 per load or £14.25 per week'},
        {'name': 'Housekeeping Services', 'description': 'Available on request: £4.75 basic cleaning or £19.00 per week'}
    ]
    
    # Meal plans data
    meal_plans = {
        'daily': {
            'breakfast': 3.80,
            'lunch': 5.70,
            'dinner': 5.70,
            'full_day': 14.25
        },
        'weekly': {
            'breakfast': 24,
            'lunch': 36,
            'dinner': 36,
            'full_day': 90
        },
        'monthly': {
            'breakfast': 95,
            'lunch': 142,
            'dinner': 142,
            'full_day': 332
        }
    }
    
    # Sample meals data
    sample_meals = [
        {'name': 'Full English Breakfast', 'description': 'Eggs, bacon, sausage, baked beans, grilled tomatoes, mushrooms, and toast', 'tag': 'Breakfast', 'image': 'breakfast.jpg'},
        {'name': 'Grilled Chicken Caesar Salad', 'description': 'Fresh romaine lettuce, grilled chicken breast, parmesan cheese, croutons, and Caesar dressing', 'tag': 'Lunch', 'image': 'lunch.jpg'},
        {'name': 'Grilled Salmon', 'description': 'Fresh Atlantic salmon with roasted vegetables and herb butter sauce', 'tag': 'Dinner', 'image': 'dinner1.jpg'},
        {'name': 'Beef Wellington', 'description': 'Tender beef fillet wrapped in puff pastry with mushroom duxelles', 'tag': 'Dinner', 'image': 'dinner2.jpg'},
        {'name': 'Butternut Squash Risotto', 'description': 'Creamy arborio rice with roasted butternut squash, sage, and parmesan', 'tag': 'Vegetarian', 'image': 'vegetarian.jpg'},
        {'name': 'Chocolate Lava Cake', 'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream', 'tag': 'Dessert', 'image': 'dessert.jpg'}
    ]
    
    return render_template('amenities.html', amenities=amenities_data, meal_plans=meal_plans,sample_meals=sample_meals)