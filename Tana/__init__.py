#!/usr/bin/python3
"""Module for the Tana package"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from Tana.config import Config
from Tana.engine.storage import DBStorage
from Tana.models.base_model import Base

db_storage = DBStorage()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
cors = CORS()
mail = Mail()
jwt = JWTManager()
@login_manager.user_loader
def load_user(users):
    """Load user function"""
    return db_storage.get(users, users.id)



def create_app(config_class=Config):
    """Creates the app"""
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db_storage
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from Tana.users.routes import Users
    from Tana.functions.routes import functions
    from Tana.offices.routes import offices
    from Tana.reminder.routes import reminders
    from Tana.humanresource.routes import humanresource



    app.register_blueprint(Users)
    app.register_blueprint(functions)
    app.register_blueprint(offices)
    app.register_blueprint(reminders)
    app.register_blueprint(humanresource)

    return app

