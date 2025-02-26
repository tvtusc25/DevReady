"""This module contains a function for initializing DevReady."""
import os
from flask import Flask
from dotenv import load_dotenv
from .views import main_blueprint
load_dotenv()

def create_app():
    """Creates the Flask application."""
    app = Flask(__name__)
    app.config["API_KEY"] = os.getenv("API_KEY")

    # Register blueprint for routes
    app.register_blueprint(main_blueprint)

    return app