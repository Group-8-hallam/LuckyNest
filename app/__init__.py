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

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from .routes.auth import auth_bp
    from .routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    from .routes.pg import pg_bp
    app.register_blueprint(pg_bp, url_prefix='/pg')

    from .routes.rooms import rooms_bp
    app.register_blueprint(rooms_bp, url_prefix='/rooms')

    return app