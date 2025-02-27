"""This module contains endpoints for DevReady"""
import os
from flask import Blueprint, render_template, jsonify
from flask import request
from openai import OpenAI

ds_key = os.environ.get('deepseek_key')
client = OpenAI(api_key=ds_key, base_url="https://api.deepseek.com")

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

API_KEY = os.getenv("API_KEY")

@main_blueprint.route('/', methods=['GET', 'POST'])
def main():
    """Endpoint to get main page."""
    return render_template('index.html')


@main_blueprint.route('/library', methods=['GET', 'POST'])
def library():
    """Endpoint to get problem library page."""
    return render_template('library.html')

@main_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    """Endpoint to get profile page."""
    return render_template('profile.html')

@main_blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    """Endpoint to get settings page."""
    return render_template('settings.html')


@main_blueprint.route('/about', methods=['GET', 'POST'])
def about():
    """Endpoint to get about page."""
    return render_template('about.html')


@main_blueprint.route('/hint', methods=['POST'])
def hint():
    #these may need to change, but making assumptions about the front-end for now
    question_title = request.json.get('question_title')
    code = request.json.get('code')
    
    input = f"I am trying to solve this Leetcode question titled {question_title}, but I am stuck. This is my code so far: {code}"
    print("About to make model call")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a coding interviewer and your interviewee is stuck on a Leetcode-style problem. Evaluate their current code, determine if their are any logical mistakes, and help guide them to the right answer. DO NOT GIVE AWAY THE ANSWER. Be concise and patient. "},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        return jsonify({"success": True, "hint": response.choices[0].message.content})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500




@main_blueprint.route('/analyze_submission', methods=['POST'])
def analyze_submission():
    #these may need to change, but making assumptions about the front-end for now
    question_title = request.json.get('question_title')
    code = request.json.get('code')
    
    system_prompt = "You are a CS professor who specializes in algorithms. Evaluate a given solution to the Leetcode question, first understanding its space/time complexity, then comparing it to the optimal solution. If there are ways to improve the code, suggest them at the end of your response. Be succint."
    user_prompt = f"I just solved this Leetcode question titled {question_title}. Can you tell me about its time/space complexity, and compare it to the optimal solution? This is my code: {code}"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        print("Worked")
        return jsonify({"success": True, "hint": response.choices[0].message.content})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500

    