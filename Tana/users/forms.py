#!/bin/usr/python3
"""Forms module for the users"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.members import users
from flask_login import current_user, UserMixin, login_user, logout_user, login_required, LoginManager
from flask_wtf.file import FileField, FileAllowed
from Tana.engine.storage import DBStorage
from Tana.models.roles import UserRole


# create a class to register a user by admin
class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired()])
    ID_No = StringField('ID_No', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    office_id = StringField('Office_id')
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Register')
    def validate_email(self, email):
        db_storage = DBStorage()
        user = db_storage.get(users, email=email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
    def validate_office_id(self, office_id):
        if self.role.data == 'admin' and office_id.data:
            raise ValidationError('Admins should not have an office id')
            
class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            db_storage = DBStorage()
            user = db_storage.get(users, email=email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        db_storage = DBStorage()
        user = db_storage.get(users, email=email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

