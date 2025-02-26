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