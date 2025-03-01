"""This module contains endpoints for DevReady"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def main():
    """Endpoint to get main page."""
    return render_template('index.html', user=current_user)

@main_blueprint.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    """Endpoint to get problem library page."""
    return render_template('library.html', user=current_user)

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Endpoint to get profile page."""
    return render_template('profile.html', user=current_user)

@main_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Endpoint to get settings page."""
    return render_template('settings.html', user=current_user)
