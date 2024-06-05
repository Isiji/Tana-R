#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, request, flash, render_template, redirect, url_for
from Tana.models.funcategory import FunctionCategory
from Tana.models.offices import Offices
from Tana.offices.forms import OfficeForm, LoginOfficeForm
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
        office = Offices(office_name=form.office_name.data, office_location=form.office_location.data, office_description=form.office_description.data, office_email=form.office_email.data, office_manager=form.office_manager.data, password=hashed_password)
        db_storage.new(office)
        db_storage.save()
        flash(f'Your office has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('create_office.html', title='Create Office', form=form)



#create a route for the office dashboard
@offices.route('/office_dashboard')
@login_required
def office_dashboard():
    """route for the office dashboard"""
    return render_template('office.html', title='Office Dashboard')
