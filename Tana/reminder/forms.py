# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class ReminderForm(FlaskForm):
    reminder_name = StringField('Reminder Name', validators=[DataRequired()])
    reminder_description = TextAreaField('Reminder Description', validators=[DataRequired()])
    reminder_date = DateField('Reminder Date', format='%Y-%m-%d', validators=[DataRequired()])
    reminder_time = TimeField('Reminder Time', format='%H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Set Reminder')
