#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from Tana.models.funcategory import FunctionCategory
from Tana.models.offices import Offices
from Tana.offices.forms import OfficeForm, LoginOfficeForm
from flask_login import login_required, current_user, login_user, logout_user
from Tana import bcrypt, db_storage
from Tana.models.members import users
import logging

offices = Blueprint('offices', __name__)

#create a route for creating offices by the admin
@offices.route('/create_office', methods=['POST', 'GET'])
def create_office():
    """route for creation of offices"""
    form = OfficeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        office = Offices(office_name=form.office_name.data, office_location=form.office_location.data, office_description=form.office_description.data, email=form.email.data, office_manager=form.office_manager.data, password=hashed_password)
        db_storage.new(office)
        db_storage.save()
        flash(f'Your office has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('create_office.html', title='Create Office', form=form)


#route for office dashboard


@offices.route('/office_dashboard', methods=['POST', 'GET'], strict_slashes=False)
def office_dashboard():
    """route for the office dashboard"""
    if 'user_id'in session:
        user_id = session['user_id']
        office = db_storage.get(Offices, id=user_id)
        
        if office:
            office_name = office.office_name
            office_location = office.office_location
            office_description = office.office_description
            office_manager = office.office_manager
            email = office.email
            
            return render_template('office.html', title='Office Dashboard',office=office, office_name=office_name, office_location=office_location, office_description=office_description, office_manager=office_manager, email=email)
        else:
            logging.error('Office not found. error number 1')
            
    else:
        logging.error('Office not found. error number 2')
        return redirect(url_for('main.login'))
