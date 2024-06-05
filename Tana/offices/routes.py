#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, request, flash, render_template, redirect, url_for
from Tana.models.funcategory import FunctionCategory
from Tana.models.offices import Offices
from Tana.offices.forms import OfficeForm, RegistrationForm, LoginOfficeForm
from flask_login import login_required, current_user, login_user, logout_user
from Tana import bcrypt, db_storage
from Tana.models.members import users

offices = Blueprint('offices', __name__)

#create a route for creating offices by the admin
@offices.route('/create_office', methods=['POST', 'GET'])
def create_office():
    """route for creation of offices"""
    form = OfficeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        office = Offices(office_name=form.office_name.data, office_location=form.office_location.data, office_description=form.office_description.data, office_contact=form.office_contact.data, office_manager=form.office_manager.data, password=hashed_password)
        db_storage.new(office)
        db_storage.save()
        flash(f'Your office has been created! You are now able to log in', 'success')
        return redirect(url_for('offices.login_office'))
    return render_template('create_office.html', title='Create Office', form=form)

@offices.route('/register_admin', methods=['POST'])
@login_required
def register_admin():
    """route for registration of admins"""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = db_storage.get(users, email=form.email.data)
        if user:
            flash('That email is taken. Please choose a different one.', 'danger')
            return redirect(url_for('offices.register_admin'))
        user = users(name=form.name.data, email=form.email.data, role=form.role.data, password=hashed_password, phone=form.phone.data, ID_No=form.ID_No.data, office_id=form.office_id.data)
        db_storage.new(user)
        db_storage.save()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('Users.login'))
    return render_template('register_admin.html', title='Register Admin', form=form)

#create a route to login an office
@offices.route('/login_office', methods=['POST', 'GET'])
def login_office():
    """route for logging in an office"""
    form = LoginOfficeForm()
    if form.validate_on_submit():
        office = db_storage.get(Offices, office_name=form.office_name.data)
        if office and bcrypt.check_password_hash(office.password, form.password.data):
            login_user(office)
            return redirect(url_for('offices.office'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login_office.html', title='Login Office', form=form)