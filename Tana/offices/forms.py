from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.offices import Offices
from Tana.models.members import users
from Tana.models.humanresource import HumanResource
from Tana.models.functions import Functions
from Tana.models.contributions import Contributions
from Tana.models.tasks import Tasks
from Tana.models.attendees import Attendees
from Tana.models.diary import Diary
from Tana.models.commitments import Commitments
from Tana.models.calendarEvents import CalendarEvents
from Tana.models.reminder import Reminder
from Tana.models.roles import UserRole
from Tana.models.funcategory import FunctionCategory
from Tana.models.impactlevel import ImpactLevel
from Tana import bcrypt, db_storage
from flask_login import login_required, current_user, login_user, logout_user
from  flask_wtf.file import FileField, FileAllowed

#crreate a class to register an office
class OfficeForm(FlaskForm):
    office_name = StringField('Office Name', validators=[DataRequired()])
    office_location = StringField('Office Location', validators=[DataRequired()])
    office_description = StringField('Office Description', validators=[DataRequired()])
    office_contact = StringField('Office Contact', validators=[DataRequired()])
    office_manager = StringField('Office Manager', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Office')


class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired()])
    ID_No = StringField('ID_No', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    office_id = StringField('Office_id')
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Register')
    def validate_email(self, email):
        user = db_storage.get(users, email=email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
    def validate_office_id(self, office_id):
        if self.role.data == 'admin' and office_id.data:
            raise ValidationError('Admins should not have an office id')
