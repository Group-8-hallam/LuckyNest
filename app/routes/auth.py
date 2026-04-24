from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pg.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('pg.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pg.dashboard'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=hashed_password,
            role='pg'
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created! Please select a room to complete your booking.', 'success')
        return redirect(url_for('pg.book_room'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

def dashboard_redirect():
    return redirect(url_for('pg.dashboard'))