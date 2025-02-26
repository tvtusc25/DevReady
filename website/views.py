"""This module contains endpoints for DevReady"""
import os
from flask import Blueprint, render_template, jsonify
from flask import request

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

API_KEY = os.getenv("API_KEY")

@main_blueprint.route('/', methods=['GET', 'POST'])
def main():
    """Endpoint to get main page."""
    return render_template('index.html')