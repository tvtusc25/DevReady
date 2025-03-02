"""Unit tests for code execution API."""
import subprocess
from website.code_execution import execute_code

def test_python_execution(mock_subprocess_run):
    """Test Python code execution returns expected output."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["python3"], returncode=0, stdout="Hello, Python!"
    )
    output, rc = execute_code(["python3", "-c", "print('Hello, Python!')"])

    assert rc == 0
    assert output == "Hello, Python!"

def test_execution_timeout(mock_subprocess_run):
    """Test handling of execution timeouts."""
    mock_subprocess_run.side_effect = subprocess.TimeoutExpired(cmd="python3", timeout=5)

    output, rc = execute_code(["python3", "-c", "while True: pass"])

    assert rc == 1
    assert "Execution timed out" in output
