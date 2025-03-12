import pytest
from flask import url_for
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()
        
        # Remove existing test user if present
        User.query.filter_by(mobile='9326913788').delete()
        db.session.commit()
        
        # Add test user
        test_user = User(
            username='vihaan_shetty',
            mobile='9326913788',
            password=generate_password_hash('pass', method='pbkdf2:sha256'),
            pin=generate_password_hash('1716', method='pbkdf2:sha256'),
            age=35, gender='M', account='1236578', balance=100.0
        )
        db.session.add(test_user)
        db.session.commit()
    
    yield app.test_client()
    
    # Cleanup database after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

# Test for valid login
def test_login(client):
    response = client.post('/login', data={'username': 'vihaan_shetty', 'password': 'pass'}, follow_redirects=True)
    assert b'Invalid username or password' not in response.data
    assert b'Welcome' in response.data  # Adjust based on your success message

# Test for invalid login
def test_invalid_login(client):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Invalid username or password' in response.data

# Test for user registration
def test_register(client):
    with client.application.app_context():
        # Remove test user if exists
        User.query.filter_by(mobile="8888888888").delete()
        db.session.commit()
    import pytest
from flask import url_for
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()
        
        # Remove existing test user if present
        User.query.filter_by(mobile='9326913788').delete()
        db.session.commit()
        
        # Add test user
        test_user = User(
            username='vihaan_shetty',
            mobile='9326913788',
            password=generate_password_hash('pass', method='pbkdf2:sha256'),
            pin=generate_password_hash('1716', method='pbkdf2:sha256'),
            age=35, gender='M', account='1236578', balance=100.0
        )
        db.session.add(test_user)
        db.session.commit()
    
    yield app.test_client()
    
    # Cleanup database after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

# Test for valid login
def test_login(client):
    response = client.post('/login', data={'username': 'vihaan_shetty', 'password': 'pass'}, follow_redirects=True)
    assert b'Invalid username or password' not in response.data
    assert b'Welcome' in response.data  # Adjust based on your success message

# Test for invalid login
def test_invalid_login(client):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Invalid username or password' in response.data

# Test for user registration
def test_register(client):
    with client.application.app_context():
        # Remove test user if exists
        User.query.filter_by(mobile="8888888888").delete()
        db.session.commit()
    
    # Register the new user
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

    # Register the new user 
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
