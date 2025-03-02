"""Methods for code execution"""
import os
import subprocess
import tempfile
import shutil
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from website.models import Question, Submission
from website.extensions import db

code_exec_blueprint = Blueprint("code_exec", __name__)

def execute_code(command, timeout=5):
    """Executes a command in a subprocess and returns its output and return code."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        return (result.stdout if result.returncode == 0 else result.stderr, result.returncode)
    except subprocess.TimeoutExpired:
        return ("Execution timed out", 1)
    except Exception as e:
        return (str(e), 1)

def execute_code_with_test(code, test_input, expected_method):
    """Runs code on a given test input and returns the result."""
    temp_dir = tempfile.mkdtemp()
    try:
        imports = (
            "from typing import List, Dict, Tuple\n"
            "import math\n"
            "import heapq\n"
            "import bisect\n"
            "import collections\n"
            "import itertools\n"
            "import string\n"
            "import re\n"
            "import random\n"
            "import time\n"
            "import sys\n"
            "import json\n"
            "import functools\n"
            "import operator\n"
        )

        runner = (
            "\nif __name__ == '__main__':\n"
            "    import sys, json\n"
            "    data = sys.stdin.read().strip()\n"
            "    args = json.loads(data)\n"
            "    sol = Solution()\n"
            f"    result = sol.{expected_method}(args)\n"
            "    print(json.dumps(result))\n"  # Print as JSON
        )

        full_code = imports + code + runner
        code_file = os.path.join(temp_dir, "solution.py")

        with open(code_file, "w", encoding="utf-8") as f:
            f.write(full_code)

        process = subprocess.run(
            ["python3", code_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        if process.returncode != 0:
            # Extract just the last line from stderr (usually the error message)
            err_lines = process.stderr.strip().splitlines()
            error_message = err_lines[-1] if err_lines else "Unknown error occurred."
            return {"error": error_message}

        # Parse and return the output as a proper type
        return json.loads(process.stdout.strip())

    finally:
        shutil.rmtree(temp_dir)


def run_tests(code, test_cases, expected_method):
    """Runs the given user code against question's test cases."""
    results = []
    all_passed = True

    for test in test_cases:
        actual_output = execute_code_with_test(code, test.inputData, expected_method)
        expected = json.loads(test.expectedOutput)
        passed = actual_output == expected

        results.append({
            "passed": passed,
            "input": test.inputData if test.isSample else "Hidden",
            "expected": test.expectedOutput if test.isSample else "Hidden",
            "actual": actual_output if test.isSample else "Hidden"
        })

        if not passed:
            all_passed = False

    return results, all_passed


@code_exec_blueprint.route("/run/<int:question_id>", methods=["POST"])
@login_required
def run_code_samples(question_id):
    """Runs user's code against sample test cases when called."""
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        question = Question.query.get_or_404(question_id)
        sample_tests = [test for test in question.testCases if test.isSample]
        results, all_passed = run_tests(code, sample_tests, question.expected_method)

        return jsonify({
            "passed": all_passed,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": f"Error running sample tests: {str(e)}"}), 500

@code_exec_blueprint.route("/submit/<int:question_id>", methods=["POST"])
@login_required
def submit_solution(question_id):
    """Runs submitted code against test cases, returning results."""
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    question = Question.query.get_or_404(question_id)
    results, all_passed = run_tests(code, question.testCases, question.expected_method)

    try:
        submission = Submission(
            userID=current_user.userID,
            questionID=question_id,
            code=code,
            result="Passed" if all_passed else "Failed",
            language="python"
        )
        db.session.add(submission)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to save submission: {str(e)}"}), 500

    return jsonify({
        "passed": all_passed,
        "results": results
    })
