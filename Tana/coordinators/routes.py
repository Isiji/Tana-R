#!/usr/bin/python3
"""routes for the coordinators"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.coordinators.forms import CountyOfficeUpdateForm
from Tana.models.county_office_update import CountyOfficeUpdate

coordinators = Blueprint('coordinators', __name__)

@coordinators.route('/coordinator_dashboard')
@login_required
def coordinator_dashboard():
    """route for the coordinator dashboard"""
    return render_template('coordinator.html', title='Coordinator Dashboard')


@coordinators.route('/add_county_office_update', methods=['GET', 'POST'])
@login_required
def add_county_office_update():
    """Route to add a county office update."""
    form = CountyOfficeUpdateForm()
    if form.validate_on_submit():
        update = CountyOfficeUpdate(
            date=form.date.data,
            party_involved=form.party_involved.data,
            issues=form.issues.data,
            delegation=form.delegation.data,
            contact_person=form.contact_person.data,
            action_taken=form.action_taken.data
        )
        db_storage.new(update)
        db_storage.save()
        flash('County office update has been submitted!', 'success')
        return redirect(url_for('coordinator.view_county_office_updates'))
    return render_template('county_office_update_form.html', title='Add County Office Update', form=form)

@coordinators.route('/view_county_office_updates', methods=['GET'])
@login_required
def view_county_office_updates():
    """Route to view all county office updates."""
    updates = db_storage.all(CountyOfficeUpdate)  # Adjust according to your db_storage methods
    return render_template('view_county_office_updates.html', title='County Office Updates', updates=updates)