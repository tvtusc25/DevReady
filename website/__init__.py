"""This module contains a function for initializing DevReady."""
import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .auth import auth_blueprint
from .views import main_blueprint
from .code_execution import code_exec_blueprint
from .ai_helper import ai_helper_blueprint
from .models import User
from .extensions import db

load_dotenv()

def create_app():
    """Creates the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL') or 'sqlite:///devready.db'
    app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.register'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_blueprint)
    app.register_blueprint(code_exec_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(ai_helper_blueprint)

    with app.app_context():
        db.create_all() # Create tables (if not created)
    return app
