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
from Tana.models.members import users

db_storage = DBStorage()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Users.login'
#login_manager.login_view = 'offices.login_office'
login_manager.login_message_category = 'info'
cors = CORS()
mail = Mail()
jwt = JWTManager()
@login_manager.user_loader
def load_user(users):
    """Load user function"""
    user = db_storage.get_user(users)
    if user:
        return user
    else:
        office = db_storage.get_office(users)
        if office:
            return office
    return None





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
    
    with app.app_context():
       db_storage.reload()
       
       if not db_storage.get_user('ziggy@gmail.com'):
           users.create_super_admin()


    from Tana.users.routes import Users
    from Tana.functions.routes import functions
    from Tana.offices.routes import offices
    from Tana.reminder.routes import reminders
    from Tana.humanresource.routes import humanresource
    from Tana.main.routes import main
    from Tana.reminder.routes import reminders
    from Tana.bodyguards.routes import bodyguards
    from Tana.secretaries.routes import secretaries
    from Tana.coordinators.routes import coordinators
    from Tana.drivers.routes import drivers
    from Tana.chief_field_officers.routes import chieffieldofficers
    from Tana.field_officers.routes import fieldofficers
    from Tana.researchers.routes import researchers
    from Tana.others.routes import others
    from Tana.bills.routes import bills
    from Tana.legislation.routes import legislation
    from Tana.oversight.routes import oversight
    



    app.register_blueprint(Users)
    app.register_blueprint(functions)
    app.register_blueprint(offices)
    app.register_blueprint(reminders)
    app.register_blueprint(humanresource)
    app.register_blueprint(main)
    app.register_blueprint(bodyguards)
    app.register_blueprint(secretaries)
    app.register_blueprint(coordinators)
    app.register_blueprint(drivers)
    app.register_blueprint(chieffieldofficers)
    app.register_blueprint(fieldofficers)
    app.register_blueprint(researchers)
    app.register_blueprint(others)
    app.register_blueprint(bills)
    app.register_blueprint(legislation)
    app.register_blueprint(oversight)
    
   
    
    return app

