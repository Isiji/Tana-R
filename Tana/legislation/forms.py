#!/usr/bin/python3
"""forms for the legislation"""
from flask_wtf import FlaskForm
from wtforms import StringField,DateField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

class MotionsForm(FlaskForm):
    """Motions form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class StatementsForm(FlaskForm):
    """Statements form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')
class LegislationForm(FlaskForm):
    """Legislation form"""
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

#class to add motion from motion class and document should be a file
class AddMotionForm(FlaskForm):
    """Add motion form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')
class QuestionsForm(FlaskForm):
    """Questions form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')





