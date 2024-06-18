#!/usr/bin/python3
"""Forms for the bills"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateField, SelectField
from wtforms.validators import DataRequired

class BillsForm(FlaskForm):
    """ form for adding bills"""
    bill_name = StringField('Bill Name', validators=[DataRequired()])
    submitted_date = DateField('Submitted Date', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    status = SelectField('Status', choices=[('First Reading', 'First Reading'),
                                            ('Second Reading', 'Second Reading'),
                                            ('Third Reading', 'Third Reading'),
                                            ('Presidential Assent', 'Presidential Assent'),
                                            ('Commencement', 'Commencement')], validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    