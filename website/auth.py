"""Blueprint for authentication."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User
from .extensions import db
from .models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Endpoint to get login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User.query.filter_by(email=username).first()
        if user and check_password_hash(user.passwordHash, password):
            login_user(user, remember=remember)
            return redirect(url_for('main.main'))
        if not user:
            flash("We couldn't find an account with that email address.", "danger")
        else:
            flash("The password you entered is incorrect.", "danger")
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Endpoint to get register page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("Username taken.", "danger")
            return redirect(url_for('auth.register'))

        if len(password) > 20 or len(password) < 8:
            flash("Password must be between 8 and 20 characters.", "danger")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Passwords must match.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(username = username,
                        email = email,
                        passwordHash = generate_password_hash(password, "pbkdf2"))
        try:
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Error creating user: " + str(e))
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@auth_blueprint.route('/about', methods=['GET', 'POST'])
def about():
    """Endpoint to get about page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    return render_template('about.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    """Endpoint to logout."""
    logout_user()
    return redirect(url_for('auth.login'))
