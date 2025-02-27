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

def test_cpp_execution(mock_subprocess_run, client):
    """Test C++ code execution returns expected output."""
    # Simulate successful compilation
    def mock_cpp_run(args):
        if "g++" in args:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="")
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="Hello, C++!")

    mock_subprocess_run.side_effect = mock_cpp_run

    response = client.post("/run", json={
        "language": "cpp",
        "code": '#include<iostream>\nint main(){ std::cout << "Hello, C++!"; return 0; }'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "output" in data
    assert data["output"] == "Hello, C++!"

def test_javascript_execution(mock_subprocess_run, client):
    """Test JavaScript code execution returns expected output."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=["node"], returncode=0,
                                                                   stdout="Hello, Javascript!")

    response = client.post("/run", json={
        "language": "javascript",
        "code": 'console.log("Hello, Javascript!");'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "output" in data
    assert data["output"] == "Hello, Javascript!"

def test_java_execution(mock_subprocess_run, client):
    """Test Java code execution returns expected output."""
    def mock_java_run(args):
        if "javac" in args:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="")
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="Hello, Java!")

    mock_subprocess_run.side_effect = mock_java_run

    response = client.post("/run", json={
        "language": "java",
        "code": ('public class Solution { public static void main(String[] args) { '
                 'System.out.println("Hello, Java!"); } }')
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "output" in data
    assert data["output"] == "Hello, Java!"

def test_swift_execution(mock_subprocess_run, client):
    """Test Swift code execution returns expected output."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=["swift"], returncode=0,
                                                                   stdout="Hello, Swift!")

    response = client.post("/run", json={
        "language": "swift",
        "code": 'print("Hello, Swift!")'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "output" in data
    assert data["output"] == "Hello, Swift!"

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

def test_invalid_language(client):
    """Test API response for unsupported language."""
    response = client.post("/run", json={
        "language": "fortran",
        "code": "PRINT *, 'Hello, Fortran!'"
    })

    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data
    assert "Invalid request" in data["error"]
