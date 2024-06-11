#!/usr/bin/python3
"""forms for the oversight"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class OversightForm(FlaskForm):
    """Oversight form"""
    document = StringField('Document', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')




