#!/bin/usr/python3
"""Forms module for the users"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.members import users
from flask_login import current_user, UserMixin, login_user, logout_user, login_required, LoginManager
from flask_wtf.file import FileField, FileAllowed
from Tana import bcrypt, db_storage
from Tana.models.roles import UserRole


# create a class to register a user by admin
class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired()])
    ID_No = StringField('ID No', validators=[DataRequired()])
    role = SelectField('Role', choices=[(role.value, role.name.replace('_', ' ').title()) for role in UserRole], validators=[DataRequired()])
    office_id = StringField('Office ID', validators=[])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = db_storage.get(users, email=email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
    def validate_office_id(self, office_id):
        if self.role.data == UserRole.SUPER_ADMIN.value and office_id.data:
            raise ValidationError('Admins should not have an office ID.')            
class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db_storage.get(users, email=email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = db_storage.get(users, email=email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_email(self, email):
        user = db_storage.get(users, email=email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
        