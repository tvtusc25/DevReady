"""This module handles secure code execution for DevReady."""
import os
import subprocess
import tempfile
from flask import Blueprint, request, jsonify

code_exec_blueprint = Blueprint("code_exec", __name__)

# Supported languages and their execution commands
EXECUTION_COMMANDS = {
    "python": ["python3"],
    "javascript": ["node"],
    "cpp": ["g++", "./a.out"],
    "java": ["javac", "java"],
    "swift": ["swift"]
}

def execute_code(command, timeout=5):
    """Executes a given command in a subprocess and returns the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return (result.stdout if result.returncode == 0 else result.stderr, result.returncode)
    except subprocess.TimeoutExpired:
        return ("Execution timed out", 1)
    except Exception as e:
        return (str(e), 1)

@code_exec_blueprint.route("/run", methods=["POST"])
def run_code():
    """Endpoint to execute submitted code securely."""
    data = request.get_json()
    code, language = data.get("code"), data.get("language")

    if not code or language not in EXECUTION_COMMANDS:
        return jsonify({"error": "Invalid request"}), 400

    temp_dir = tempfile.mkdtemp()  # Use a directory for safety
    temp_file_path = os.path.join(temp_dir, f"Solution.{language}")

    try:
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(code)

        if language == "python":
            output, returncode = execute_code(["python3", temp_file_path])

        elif language == "javascript":
            output, returncode = execute_code(["node", temp_file_path])

        elif language == "cpp":
            compile_output, compile_code = execute_code(["g++", temp_file_path, "-o", f"{temp_dir}/a.out"])
            if compile_code != 0:
                return jsonify({"error": compile_output}), 400
            output, returncode = execute_code([f"{temp_dir}/a.out"])

        elif language == "java":
            java_file = os.path.join(temp_dir, "Solution.java")
            os.rename(temp_file_path, java_file)
            compile_output, compile_code = execute_code(["javac", java_file])
            if compile_code != 0:
                return jsonify({"error": "Java compilation failed: " + compile_output}), 400
            output, returncode = execute_code(["java", "-cp", temp_dir, "Solution"])

        elif language == "swift":
            output, returncode = execute_code(["swift", temp_file_path])

        else:
            return jsonify({"error": "Unsupported language"}), 400

        if returncode == 0:
            return jsonify({"output": output}), 200 
        else:
            return jsonify({"error": output}), 400

    finally:
        # Ensure cleanup of temp directory and files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(temp_dir)
