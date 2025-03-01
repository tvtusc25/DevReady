"""Configuration for pytest fixtures."""
import pytest
from website import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # In-memory database for tests
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Set up a test client for the Flask app."""
    return app.test_client()

@pytest.fixture
def mock_subprocess_run(mocker):
    """Fixture to mock subprocess.run for safe code execution testing."""
    return mocker.patch("subprocess.run")
