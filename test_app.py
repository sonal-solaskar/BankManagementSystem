import pytest
from flask import url_for
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
    
    with app.app_context():
        db.create_all()
        test_user = User(username='vihaan_shetty', mobile='9326913788',
                         password=generate_password_hash('pass', method='pbkdf2:sha956'),
                         pin=generate_password_hash('1716', method='pbkdf2:sha956'),
                         age=35, gender='M', account='1236578', balance=100.0)
        db.session.add(test_user)
        db.session.commit()

    yield app.test_client()

# Authentication Tests
def test_login(client):
    response = client.post('/login', data={'username': 'vihaan_shetty', 'password': 'pass'}, follow_redirects=True)
    assert b'Invalid username or password' not in response.data

def test_invalid_login(client):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Invalid username or password' in response.data

def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'mobile': '8888888888',
        'password': 'newpass123',
        'pin': '1234',
        'age': '22',
        'gender': 'F',
        'account': '87654321'
    }, follow_redirects=True)
    assert b'Account Successfully created' in response.data

# Transaction Tests
def test_deposit(client):
    response = client.post('/deposit', data={'deposit': '500', 'pin': '1234'}, follow_redirects=True)
    assert b'Deposit successful' in response.data

def test_invalid_withdraw(client):
    response = client.post('/withdraw', data={'withdraw': '2000', 'pin': '1234'}, follow_redirects=True)
    assert b'Insufficient balance' in response.data

def test_valid_withdraw(client):
    response = client.post('/withdraw', data={'withdraw': '200', 'pin': '1234'}, follow_redirects=True)
    assert b'Withdrawal successful' in response.data

def test_transfer(client):
    response = client.post('/transfer', data={'transfer': '100', 'toid': '2', 'pin': '1234'}, follow_redirects=True)
    assert b'Transfer successful' in response.data

# Account Tests
def test_account_page(client):
    response = client.get('/account')
    assert response.status_code == 200

def test_transaction_page(client):
    response = client.get('/transactions')
    assert response.status_code == 200
