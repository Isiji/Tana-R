#!/usr/bin/env python3
"""Users route for the users"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana.engine.storage import DBStorage
from Tana.users.forms import UpdateAccountForm, RequestResetForm, LoginForm,ResetPasswordForm, RegistrationForm, EmployeeRegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from Tana import bcrypt, db_storage
from Tana.models.employee_register import EmployeeRegister


Users = Blueprint('Users', __name__)

# create a route for homepage
@Users.route('/')
@Users.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')

# create route for user to update user information
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
        return redirect(url_for('Users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

#create route for admin dashboard
@Users.route('/admin_dashboard', methods=['POST', 'GET'], strict_slashes=False)
def admin_dashboard():
    """route for the admin dashboard"""
    if current_user.is_authenticated:
        if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value):
            return render_template('admin_dashboard.html', title='Admin Dashboard')
        else:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.home'))
    else:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('Users.login'))
    

@Users.route('/register', methods=['GET', 'POST'],strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users.create_user(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            ID_No=form.ID_No.data,
            role=form.role.data,
            office_id=form.office_id.data if form.office_id.data else None
        )
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('Users.login'))
    return render_template('register.html', title='Register', form=form)

@Users.route('/login', methods=['GET', 'POST'])
def login():
    from Tana import db_storage
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_storage.get(users, email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@Users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#route for employee register using employee register form
@Users.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
    """route for the employee register"""
    form = EmployeeRegisterForm()
    if form.validate_on_submit():
        employee = EmployeeRegister(name=form.name.data, time_in=form.time_in.data, time_out=form.time_out.data, date=form.date.data, status=form.status.data)
        db_storage.save(employee)
        flash('Registered!', 'success')
        return redirect(url_for('Users.employee_register'))
    return render_template('employee_register.html', title='Employee Register', form=form)


