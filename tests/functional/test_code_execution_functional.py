"""Functional tests for the code execution API."""
import pytest
import platform

def test_python_execution(client):
    """Test running Python code through the API."""
    response = client.post("/run", json={
        "language": "python",
        "code": "print('Hello, Python!')"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, Python!" in data["output"]

def test_timeout(client):
    """Test handling long-running code execution."""
    response = client.post("/run", json={
        "language": "python",
        "code": "while True: pass"
    })
    data = response.get_json()
    assert response.status_code == 400
    assert "Execution timed out" in data["error"]
