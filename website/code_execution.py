"""This module handles secure Python code execution for DevReady."""
import os
import subprocess
import tempfile
from flask import Blueprint, request, jsonify

code_exec_blueprint = Blueprint("code_exec", __name__)

def execute_code(command, timeout=5):
    """Executes a given command in a subprocess and returns the output."""
    try:
        result = subprocess.run(command,
                                capture_output=True,
                                text=True,
                                timeout=timeout,
                                check=False)
        return (result.stdout if result.returncode == 0 else result.stderr, result.returncode)
    except subprocess.TimeoutExpired:
        return ("Execution timed out", 1)
    except Exception as e:
        return (str(e), 1)

@code_exec_blueprint.route("/run", methods=["POST"])
def run_code():
    """Endpoint to execute submitted Python code securely."""
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "Solution.py")

    try:
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(code)

        output, returncode = execute_code(["python3", temp_file_path])

        if returncode == 0:
            return jsonify({"output": output}), 200
        return jsonify({"error": output}), 400

    finally:
        # Ensure cleanup of temp directory and files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(temp_dir)
