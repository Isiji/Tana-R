#!/usr/bin/python3
"""forms for the events"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.events import Events
from Tana.models.eventcategory import EventCategory
from Tana import db_storage, bcrypt


# create a class to register a event
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_description = TextAreaField('Event Description', validators=[DataRequired()])
    impact_level = StringField('Impact Level', validators=[DataRequired()])
    event_owner = StringField('Event Owner', validators=[DataRequired()])
    event_location = StringField('Event Location', validators=[DataRequired()])
    event_contact = StringField('Event Contact', validators=[DataRequired()])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    polling_station_name = SelectField('Polling Station', validators=[DataRequired()], choices=[])
    submit = SubmitField('Register event')

#create a form to view events that have been created

