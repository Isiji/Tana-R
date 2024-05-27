#!/usr/bin/python3
"""Forms module for the human resource"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.humanresource import HumanResource

# create a class to register a human resource
class HumanResourceForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    office_id = IntegerField('Office ID', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    employment_date = StringField('Employment Date', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    submit = SubmitField('Register Human Resource')

class UpdateHumanResourceForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    office_id = IntegerField('Office ID', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    employment_date = StringField('Employment Date', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    submit = SubmitField('Update Human Resource')

class HumanResourceSearchForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Search User')

#class to delete a user
class DeleteHumanResourceForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Delete User')

#class to search for a user
class SearchHumanResourceForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Search User')

