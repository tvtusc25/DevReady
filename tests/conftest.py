"""Configuration for pytest fixtures."""
import pytest
from website import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
    }

    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client(use_cookies=True)

@pytest.fixture
def mock_subprocess_run(mocker):
    """Fixture to mock subprocess.run for safe code execution testing."""
    return mocker.patch("subprocess.run")
