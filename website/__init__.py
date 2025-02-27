"""This module contains a function for initializing DevReady."""
import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()

def create_app():
    """Creates the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'secret keyyyyy'
    app.config["API_KEY"] = os.getenv("API_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL') or 'sqlite:///mydatabase.db'
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.register'
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .auth import auth_blueprint
    from .views import main_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    # if __name__ == '__main__':
    with app.app_context():

        db.create_all()  # Create tables (if not created)
    return app