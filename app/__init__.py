from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = 'dev-secret-change-later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///luckynest.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

   
    from .models import (
        User,
        Room,
        Booking,
        Payment,
        MealPlan,
        ServiceRequest,
        Visitor,
        Notification
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    with app.app_context():
        db.create_all()

    
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.pg import pg_bp
    from .routes.rooms import rooms_bp
    from .routes.booking import booking_bp
    from .routes.settings import settings_bp   

   
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(pg_bp, url_prefix='/pg')
    app.register_blueprint(rooms_bp, url_prefix='/rooms')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(settings_bp)        

    return app