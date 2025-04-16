import pytest
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    
    with app.app_context():
        db.create_all()
        # Create test user
        test_user = User(
            username='testuser', 
            mobile='1234567890',
            password=generate_password_hash('password123', method='pbkdf2:sha256'),
            pin=generate_password_hash('1234', method='pbkdf2:sha256'),
            age=25,
            gender='Male',
            account='Savings',
            balance=1000.0
        )
        db.session.add(test_user)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()
