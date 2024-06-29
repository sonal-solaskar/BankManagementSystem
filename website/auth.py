from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User, db
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid username or password.', category='lerror')
    
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        pin = request.form.get('pin')
        age = request.form.get('age')
        gender = request.form.get('gender')
        account = request.form.get('account')

        hashedpassword = generate_password_hash(password, method='pbkdf2:sha256')
        hashedpin = generate_password_hash(pin, method='pbkdf2:sha256')

        existing_user = User.query.filter_by(mobile=mobile).first()

        if existing_user:
            flash('Mobile number is already registered for another user.', category='rerror')
        elif len(username) < 4:
            flash("Username must be greater than 4 characters.", category='rerror')
        elif len(mobile) < 10:
            flash('Mobile number must be 10 digits.', category='rerror')
        elif len(password) < 6:
            flash('Length of password should be greater than 6.', category='rerror')
        elif not password.isalnum():
            flash('Password should not contain any special characters.', category='rerror')
        elif len(pin) != 4 or not pin.isdigit():
            flash('Pin should be 4 digit long.', category='rerror')
        else:
            new_user = User(username=username, mobile=mobile, password=hashedpassword, pin=hashedpin, age=age, gender=gender, account=account)
            db.session.add(new_user)
            db.session.commit()

            flash(f'Account Successfully created! {username} is Registered!', category='rsuccess')
            return redirect(url_for('auth.login'))

    return render_template("register.html")

