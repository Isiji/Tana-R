#!/usr/bin/env python3
"""Users route for the users"""


from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana.engine.storage import DBStorage
from Tana.users.forms import UpdateAccountForm, RequestResetForm, ResetPasswordForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from Tana import bcrypt, db_storage
from Tana.models.offices import Offices

Users = Blueprint('Users', __name__)

#create a route for homepage
@Users.route('/')
@Users.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')

#create a route for a user to register
    
#create route for user to update user information
@Users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """account route for the user"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        db_storage = DBStorage()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db_storage.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)    




@Users.route('/register', methods=['GET', 'POST'])
def register():
    """register route for the user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users(name=form.name.data, email=form.email.data, password=hashed_password, phone=form.phone.data, ID_No=form.ID_No.data, role=form.role.data, office_id=form.office_id.data)
        db_storage.new(user)
        db_storage.save()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)
