#!/usr/bin/python3
"""Forms module for the human resource"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.humanresource import HumanResource
from Tana.engine.storage import DBStorage
from Tana.models.offices import Offices
# create a class to register a human resource


class HumanResourceForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    employment_date = StringField('Employment Date', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('employee', 'Employee')], validators=[DataRequired()])
    office_id = IntegerField('Office ID', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_office_id(self, office_id):

        db_storage = DBStorage()
        office = db_storage.get(Offices, id=office_id.data)
        if not office:
            raise ValidationError('That office does not exist. Please choose a different one.')