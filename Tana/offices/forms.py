from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
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

#crreate a class to register an office
class OfficeForm(FlaskForm):
    office_name = StringField('Office Name', validators=[DataRequired()])
    office_location = StringField('Office Location', validators=[DataRequired()])
    office_description = StringField('Office Description', validators=[DataRequired()])
    office_contact = StringField('Office Contact', validators=[DataRequired()])
    submit = SubmitField('Register Office')

    