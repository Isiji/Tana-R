#!/usr/bin/env python3
"""Users route for the users"""


from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from Tana.models.users import users
from Tana.models.roles import UserRole
from Tana.engine.storage import DBStorage
from Tana.users.forms import RegistrationForm, UpdateAccountForm, loginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from Tana import bcrypt


users = Blueprint('users', __name__)

#create a route for homepage
users.route('/')
def home():
    """homepage route for the user"""
    return render_template('home.html')

#create a route for a user to register
@users.route('/register', methods=['GET', 'POST'])
def register():
    """register route for the user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        db_storage = DBStorage()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users(username=form.username.data, email=form.email.data, password=hashed_password)
        db_storage.add(user)
        db_storage.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
#create route for user to update user information
@users.route('/account', methods=['GET', 'POST'])
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

#create a route for a user to login
@users.route('/login', methods=['GET', 'POST'])
def login():
    """login route for the user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = loginForm()
    if form.validate_on_submit():
        db_storage = DBStorage()
        user = db_storage.get(users, email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#create a route for a user to logout
@users.route('/logout')
def logout():
    """logout route for the user"""
    logout_user()
    return redirect(url_for('main.home'))

