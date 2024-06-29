from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, User, Transactions
from werkzeug.security import check_password_hash

views = Blueprint('views',__name__)

@views.route('/home')
@login_required
def home():
    return render_template('base.html', user=current_user)

@views.route('/account')
@login_required
def account():
    user = current_user
    return render_template('account.html', user=user)

@views.route('/transactions')
@login_required
def transactions():
    user = current_user
    transactions = Transactions.query.filter_by(user_id=user.id).order_by(Transactions.time.desc()).limit(10).all()
    return render_template('transactions.html', user=user, transactions=transactions)

@views.route('/')
def login():
    return render_template('login.html')

@views.route('/register')
def register():
    return render_template('register.html')

@views.route('/help')
@login_required
def help():
    return render_template('help.html')

@views.route('/faq')
@login_required
def faq():
    return render_template('faq.html')

@views.route('/plans')
@login_required
def plans():
    return render_template('plans.html')

@views.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        amount = float(request.form.get('withdraw'))
        pin = request.form.get('pin')

        if not check_password_hash(current_user.pin, pin):
            flash('Invalid PIN. Please try again.', category='werror')
        elif current_user.balance < amount:
            flash('Insufficient balance.', category='werror')
        else:
            current_user.balance -= amount
            new_transaction = Transactions(user_id=current_user.id, amt=amount, t_type='withdraw', username=current_user.username)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Withdrawal successful.', category='wsuccess')
            # return redirect(url_for('views.transactions'))

    return render_template('withdraw.html')

@views.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        amount = float(request.form.get('deposit'))
        pin = request.form.get('pin')

        if not check_password_hash(current_user.pin, pin):
            flash('Invalid PIN. Please try again.', category='derror')
        else:
            current_user.balance += amount
            new_transaction = Transactions(user_id=current_user.id, amt=amount, t_type='deposit', username=current_user.username)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Deposit successful.', category='dsuccess')
            # return redirect(url_for('views.transactions'))

    return render_template('deposit.html')

@views.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        amount = float(request.form.get('transfer'))
        to_user_id = request.form.get('toid')
        pin = request.form.get('pin')

        recipient = User.query.filter_by(id=to_user_id).first()

        if not recipient:
            flash('Recipient account does not exist.', category='terror')
        elif not check_password_hash(current_user.pin, pin):
            flash('Invalid PIN. Please try again.', category='terror')
        elif current_user.balance < amount:
            flash('Insufficient balance.', category='terror')
        else:
            current_user.balance -= amount
            recipient.balance += amount
            new_transaction = Transactions(user_id=current_user.id, amt=amount, t_type='transfer', username=current_user.username)
            db.session.add(new_transaction)
            recipient_transaction = Transactions(user_id=recipient.id, amt=amount, t_type='receive', username=recipient.username)
            db.session.add(recipient_transaction)
            db.session.commit()
            flash('Transfer successful.', category='tsuccess')
            # return redirect(url_for('views.transactions'))
    
    return render_template('transfer.html')