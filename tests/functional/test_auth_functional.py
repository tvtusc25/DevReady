"""Functional tests for the auth API endpoints."""
# pylint: disable=redefined-outer-name,unused-argument

import sys
from pathlib import Path
import pytest
from werkzeug.security import generate_password_hash, check_password_hash

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from website.models import User  # pylint: disable=wrong-import-position
from website.extensions import db  # pylint: disable=wrong-import-position

@pytest.fixture
def test_user(app):
    """Create a test user for authentication tests."""
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            passwordHash=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.query(User).delete()
        db.session.commit()

def test_login_success(client, test_user):
    """Test successful login with correct credentials."""
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

def test_login_with_email(client, test_user):
    """Test successful login using email instead of username."""
    response = client.post("/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

def test_login_wrong_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post("/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"The password you entered is incorrect" in response.data

def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    with client:
        response = client.post("/login", data={
            "username": "nonexistent",
            "password": "password123"
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.data.decode()
        assert "We couldn&#39;t find an account with that email address." in html

def test_register_success(client):
    """Test successful user registration."""
    response = client.post("/register", data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "confirmPassword": "password123"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    with client.application.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.email == "new@example.com"
        assert check_password_hash(user.passwordHash, "password123")

def test_register_existing_email(client, test_user):
    """Test registration with an existing email."""
    response = client.post("/register", data={
        "username": "newuser",
        "email": "test@example.com",
        "password": "password123",
        "confirmPassword": "password123"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/register"

def test_register_existing_username(client, test_user):
    """Test registration with an existing username."""
    response = client.post("/register", data={
        "username": "testuser",
        "email": "new@example.com",
        "password": "password123",
        "confirmPassword": "password123"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/register"

def test_register_password_mismatch(client):
    """Test registration with mismatched passwords."""
    response = client.post("/register", data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "confirmPassword": "password456"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/register"

def test_register_invalid_password_length(client):
    """Test registration with invalid password length."""
    response = client.post("/register", data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "short",
        "confirmPassword": "short"
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/register"

def test_logout(client, test_user):
    """Test user logout."""
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

def test_about_page(client):
    """Test accessing about page."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Our Vision" in response.data
    assert b"DevReady" in response.data

def test_authenticated_redirects(client, test_user):
    """Test that authenticated users are redirected from auth pages."""
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    for route in ["/login", "/register", "/about"]:
        response = client.get(route)
        assert response.status_code == 302
        assert response.headers["Location"] == "/"
