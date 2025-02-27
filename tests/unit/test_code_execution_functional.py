"""Functional tests for the code execution API."""

def test_python_execution(client):
    """Test running Python code through the API."""
    response = client.post("/run", json={
        "language": "python",
        "code": "print('Hello, Python!')"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, Python!" in data["output"]

def test_javascript_execution(client):
    """Test running JavaScript code through the API."""
    response = client.post("/run", json={
        "language": "javascript",
        "code": "console.log('Hello, JS!');"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, JS!" in data["output"]

def test_java_execution(client):
    """Test running Java code through the API."""
    java_code = """
    public class Solution {
        public static void main(String[] args) {
            System.out.println("Hello, Java!");
        }
    }
    """
    response = client.post("/run", json={
        "language": "java",
        "code": java_code
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, Java!" in data["output"]

def test_cpp_execution(client):
    """Test running C++ code through the API."""
    cpp_code = """
    #include <iostream>
    int main() {
        std::cout << "Hello, C++!" << std::endl;
        return 0;
    }
    """
    response = client.post("/run", json={
        "language": "cpp",
        "code": cpp_code
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, C++!" in data["output"]

def test_swift_execution(client):
    """Test running Swift code through the API."""
    swift_code = """
    print("Hello, Swift!")
    """
    response = client.post("/run", json={
        "language": "swift",
        "code": swift_code
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "Hello, Swift!" in data["output"]

def test_invalid_language(client):
    """Test sending an invalid language to the API."""
    response = client.post("/run", json={
        "language": "fortran",
        "code": "PRINT *, 'Hello, Fortran!'"
    })
    data = response.get_json()
    assert response.status_code == 400
    assert "Invalid request" in data["error"]

def test_timeout(client):
    """Test handling long-running code execution."""
    response = client.post("/run", json={
        "language": "python",
        "code": "while True: pass"
    })
    data = response.get_json()
    assert response.status_code == 400
    assert "Execution timed out" in data["error"]
