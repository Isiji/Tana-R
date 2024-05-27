#!/usr/bin/python3
"""forms for the functions"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.functions import Functions
from Tana.models.funcategory import FunctionCategory
from Tana.engine.storage import DBStorage


# create a class to register a function
class FunctionForm(FlaskForm):
    function_name = StringField('Function Name', validators=[DataRequired()])
    function_description = TextAreaField('Function Description', validators=[DataRequired()])
    function_impact = SelectField('Function Impact', validators=[DataRequired()], choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    function_owner = StringField('Function Owner', validators=[DataRequired()])
    function_location = StringField('Function Location', validators=[DataRequired()])
    function_contact = StringField('Function Contact', validators=[DataRequired()])
    submit = SubmitField('Register Function')



class UpdateFunctionForm(FlaskForm):
    function_name = StringField('Function Name', validators=[DataRequired()])
    function_description = TextAreaField('Function Description', validators=[DataRequired()])
    function_impact = SelectField('Function Impact', validators=[DataRequired()], choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    function_owner = StringField('Function Owner', validators=[DataRequired()])
    function_location = StringField('Function Location', validators=[DataRequired()])
    function_contact = StringField('Function Contact', validators=[DataRequired()])
    submit = SubmitField('Update Function')
    

class FunctionCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    category_description = TextAreaField('Category Description', validators=[DataRequired()])
    submit = SubmitField('Register Category')
    

