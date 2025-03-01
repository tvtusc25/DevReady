"""This module handles the endpoints related to questions."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Question, QuestionTag

questions_blueprint = Blueprint("questions", __name__)

@questions_blueprint.route("/questions", methods=["GET"])
@login_required
def get_questions():
    """Get all questions from the database, with sample test cases."""
    try:
        questions = Question.query.all()
        return jsonify([{
            **question.to_dict(),
            "tags": [tag.name for tag in question.tags],
            "sample_test_cases": [
                {"input": tc.inputData, "expected_output": tc.expectedOutput}
                for tc in question.testCases
                if tc.isSample
            ]
        } for question in questions])
    except Exception as e:
        return jsonify({"error": "Failed to fetch questions", "details": str(e)}), 500

@questions_blueprint.route("/questions/<int:question_id>", methods=["GET"])
@login_required
def get_question_by_id(question_id):
    """Get a question, with sample test cases, by its ID."""
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404
        return jsonify({
            **question.to_dict(),
            "tags": [tag.name for tag in question.tags],
            "sample_test_cases": [
                {"input": tc.inputData, "expected_output": tc.expectedOutput}
                for tc in question.testCases
                if tc.isSample
            ]
        })
    except Exception as e:
        return jsonify({"error": "Failed to fetch question", "details": str(e)}), 500

@questions_blueprint.route("/questions/tags", methods=["GET"])
@login_required
def get_questions_by_tag():
    """Get questions, with sample test cases, by a specific tag."""
    try:
        tag = request.args.get("tag")
        if not tag:
            return jsonify({"error": "Tag parameter is required"}), 400

        questions = Question.query.join(QuestionTag).filter(
            QuestionTag.tag.has(name=tag)
        ).all()
        return jsonify([{
            **question.to_dict(),
            "tags": [tag.name for tag in question.tags],
            "sample_test_cases": [
                {"input": tc.inputData, "expected_output": tc.expectedOutput}
                for tc in question.testCases
                if tc.isSample
            ]
        } for question in questions])
    except Exception as e:
        return jsonify({"error": "Failed to fetch questions by tag", "details": str(e)}), 500

