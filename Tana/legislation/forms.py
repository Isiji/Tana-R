#!/usr/bin/python3
"""forms for the legislation"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class MotionsForm(FlaskForm):
    """Motions form"""
    document = StringField('Document', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class StatementsForm(FlaskForm):
    """Statements form"""
    document = StringField('Document', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class LegislationForm(FlaskForm):
    """Legislation form"""
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

