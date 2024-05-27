#!/usr/bin/python3
"""Forms for the attendees"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.attendees import Attendees

# create a class to register an attendee
class AttendeesForm(FlaskForm):
    attendee_name = StringField('Attendee Name', validators=[DataRequired()])
    attendee_email = StringField('Attendee Email', validators=[DataRequired()])
    attendee_phone = StringField('Attendee Phone', validators=[DataRequired()])
    submit = SubmitField('Register Attendee')

class UpdateAttendeesForm(FlaskForm):
    attendee_name = StringField('Attendee Name', validators=[DataRequired()])
    attendee_email = StringField('Attendee Email', validators=[DataRequired()])
    attendee_phone = StringField('Attendee Phone', validators=[DataRequired()])
    submit = SubmitField('Update Attendee')

#class to delete an attendee
class DeleteAttendeesForm(FlaskForm):
    attendee_id = IntegerField('Attendee ID', validators=[DataRequired()])
    submit = SubmitField('Delete Attendee')

#class to search for an attendee
class SearchAttendeesForm(FlaskForm):
    attendee_id = IntegerField('Attendee ID', validators=[DataRequired()])
    submit = SubmitField('Search Attendee')

