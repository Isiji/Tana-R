from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class ReminderForm(FlaskForm):
    reminder_name = StringField('Reminder Name', validators=[DataRequired()])
    reminder_description = TextAreaField('Reminder Description', validators=[DataRequired()])
    reminder_date = DateField('Reminder Date', format='%Y-%m-%d', validators=[DataRequired()])
    reminder_time = TimeField('Reminder Time (24hr format)', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Set Reminder')

    def validate_reminder_date(self, reminder_date):
        if reminder_date.data < datetime.now().date():
            raise ValidationError('Reminder date must be in the future.')

    def validate_reminder_time(self, reminder_time):
        if reminder_time.data is None:
            raise ValidationError('Reminder time is required.')
