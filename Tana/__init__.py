import os
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
from werkzeug.utils import secure_filename
from sqlalchemy.orm import configure_mappers

db_storage = DBStorage()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Users.login'
login_manager.login_message_category = 'info'
cors = CORS()
mail = Mail()
jwt = JWTManager()

@login_manager.user_loader
def load_user(user_id):
    user = db_storage.get_user_by_id(user_id)
    if user:
        return user
    else:
        office = db_storage.get_office(users)
        if office:
            return office
    return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'csv', 'pdf'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    
    db_storage
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    with app.app_context():
       db_storage.reload()
       configure_mappers()
       
       if not db_storage.get_user('ziggy@gmail.com'):
           users.create_super_admin()

    from Tana.users.routes import Users
    from Tana.events.routes import events_bp
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
    from Tana.bills.routes import bills_bp
    from Tana.legislation.routes import legislation_bp
    from Tana.oversight.routes import oversight
    from Tana.representation.routes import representation
    from Tana.lobbying.routes import lobbying

    app.register_blueprint(Users)
    app.register_blueprint(events_bp)
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
    app.register_blueprint(bills_bp)
    app.register_blueprint(legislation_bp)
    app.register_blueprint(oversight)
    app.register_blueprint(representation)
    app.register_blueprint(lobbying)
    
    return app