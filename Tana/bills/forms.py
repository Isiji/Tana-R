#!/usr/bin/python3

"""Forms for the bills"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.bills import Bills
from flask_login import current_user

#form for for the bills class
class BillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    submitted_date = StringField('Submitted Date', validators=[DataRequired()])
    first_reading = BooleanField('First Reading')
    second_reading = BooleanField('Second Reading')
    third_reading = BooleanField('Third Reading')
    presidential_assent = BooleanField('Presidential Assent')
    commencement = BooleanField('Commencement')
    documents = FileField('Documents')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        from Tana import db_storage
        bill = db_storage.get(Bills, name=name.data)
        if bill:
            raise ValidationError('That bill is already in the system. Please choose a different name.')