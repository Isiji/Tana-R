#!/bin/usr/python3
"""Forms for the reminder"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.reminder import Reminder

# create a class to register a reminder
class ReminderForm(FlaskForm):
    reminder_name = StringField('Reminder Name', validators=[DataRequired()])
    reminder_description = TextAreaField('Reminder Description', validators=[DataRequired()])
    reminder_date = StringField('Reminder Date', validators=[DataRequired()])
    reminder_time = StringField('Reminder Time', validators=[DataRequired()])
    reminder_location = StringField('Reminder Location', validators=[DataRequired()])
    reminder_contact = StringField('Reminder Contact', validators=[DataRequired()])
    submit = SubmitField('Register Reminder')

class UpdateReminderForm(FlaskForm):
    reminder_name = StringField('Reminder Name', validators=[DataRequired()])
    reminder_description = TextAreaField('Reminder Description', validators=[DataRequired()])
    reminder_date = StringField('Reminder Date', validators=[DataRequired()])
    reminder_time = StringField('Reminder Time', validators=[DataRequired()])
    reminder_location = StringField('Reminder Location', validators=[DataRequired()])
    reminder_contact = StringField('Reminder Contact', validators=[DataRequired()])
    submit = SubmitField('Update Reminder')

class ReminderSearchForm(FlaskForm):
    reminder_id = IntegerField('Reminder ID', validators=[DataRequired()])
    submit = SubmitField('Search Reminder')

#class to delete a reminder
class DeleteReminderForm(FlaskForm):
    reminder_id = IntegerField('Reminder ID', validators=[DataRequired()])
    submit = SubmitField('Delete Reminder')
