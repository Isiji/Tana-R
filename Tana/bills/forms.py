#!/usr/bin/python3
"""Forms for the bills"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired

class BillsForm(FlaskForm):
    """Form for adding bills"""
    bill_name = StringField('Bill Name', validators=[DataRequired()])
    submitted_date = DateField('Submitted Date', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    first_reading = BooleanField('First Reading')
    second_reading = BooleanField('Second Reading')
    third_reading = BooleanField('Third Reading')
    presidential_assent = BooleanField('Presidential Assent')
    commencement = BooleanField('Commencement')
    submit = SubmitField('Submit')
