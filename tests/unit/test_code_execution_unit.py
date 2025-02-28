"""Unit tests for code execution API."""
import subprocess

def test_python_execution(mock_subprocess_run, client):
    """Test Python code execution returns expected output."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=["python3"], returncode=0,
                                                                   stdout="Hello, Python!")

    response = client.post("/run", json={
        "language": "python",
        "code": "print('Hello, Python!')"
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "output" in data
    assert data["output"] == "Hello, Python!"

def test_execution_timeout(mock_subprocess_run, client):
    """Test handling of execution timeouts."""
    mock_subprocess_run.side_effect = subprocess.TimeoutExpired(cmd="python3", timeout=5)

    response = client.post("/run", json={
        "language": "python",
        "code": "while True: pass"
    })

    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data
    assert "Execution timed out" in data["error"]
