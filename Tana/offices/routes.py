#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, request,jsonify, flash, render_template, redirect, url_for, session
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
        office = Offices(office_name=form.office_name.data, office_location=form.office_location.data, office_description=form.office_description.data, email=form.email.data, office_manager=form.office_manager.data)
        db_storage.new(office)
        db_storage.save()
        flash(f'Your office has been created! You are now able to view office details', 'success')
        return redirect(url_for('offices.office_dashboard'))
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
    
#create a route for accesing a specific office by name of the office
@offices.route('/office/<string:office_name>', methods=['POST', 'GET'], strict_slashes=False)
def office(office_name):
    """route for the office dashboard"""
    office = db_storage.get(Offices, office_name=office_name)
    if office:
        office_name = office.office_name
        office_location = office.office_location
        office_description = office.office_description
        office_manager = office.office_manager
        email = office.email
        return render_template('office.html', title='Office Dashboard',office=office, office_name=office_name, office_location=office_location, office_description=office_description, office_manager=office_manager, email=email)
    else:
        logging.error('Office not found. error number 3')
        return redirect(url_for('main.home'))
    

#function that serves offices as list
@offices.route('/offices_list', methods=['GET'])
def get_offices_list():
    """Route to fetch the list of office names"""
    try:
        offices = db_storage.all(Offices)  # Fetch all offices from the database
        print(f"Offices fetched: {offices}")  # Debug statement to check the data
        if not offices:
            return jsonify([])  # Return an empty list if no offices are found
        office_names = [office.office_name for office in offices.values()]
        return jsonify(office_names)
    except Exception as e:
        # Log the exception if there's an error
        logging.error(f"Error fetching offices: {e}")
        return jsonify([]), 500
