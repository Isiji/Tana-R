#!/usr/bin/python3
"""forms for the functions"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.events import Events
from Tana.models.funcategory import FunctionCategory
from Tana import db_storage, bcrypt


# create a class to register a function
class EventForm(FlaskForm):
    function_name = StringField('Function Name', validators=[DataRequired()])
    function_description = TextAreaField('Function Description', validators=[DataRequired()])
    function_impact = SelectField('Function Impact', validators=[DataRequired()], choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    function_owner = StringField('Function Owner', validators=[DataRequired()])
    function_location = StringField('Function Location', validators=[DataRequired()])
    function_contact = StringField('Function Contact', validators=[DataRequired()])
    submit = SubmitField('Register Function')




