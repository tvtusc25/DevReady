import pytest
from app import app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    return app.test_client()

@pytest.fixture
def mock_subprocess_run(mocker):
    """Fixture to mock subprocess.run for safe code execution testing."""
    return mocker.patch("subprocess.run")
