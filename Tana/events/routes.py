#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, current_app, jsonify, request, render_template, redirect, url_for, flash
from Tana.models.eventcategory import EventCategory
from Tana.models.events import Events
from Tana import db_storage, bcrypt
from Tana.events.forms import EventForm
from flask_login import current_user, login_required
from Tana.models.roles import UserRole
import logging


events_bp = Blueprint('events', __name__)

# create a route to add events
@events_bp.route('/add_event', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_event():
    """Route to add an event"""
    form = EventForm()
    if form.validate_on_submit():
        event_name = form.event_name.data
        event_description = form.event_description.data
        impact_level = form.impact_level.data
        event_owner = form.event_owner.data
        event_location = form.event_location.data
        event_contact = form.event_contact.data
        event_date = form.event_date.data

        event = Events(
            event_name=event_name, 
            event_description=event_description, 
            impact_level=impact_level, 
            event_owner=event_owner, 
            event_location=event_location, 
            event_contact=event_contact,
            event_date=event_date
        )

        db_storage.new(event)
        db_storage.save()

        flash('Event has been created!', 'success')
        return render_template('events.html')

    return render_template('add_event.html', title='Add Event', form=form)

def redirect_based_on_role():
    """Function to redirect based on the user role"""
    current_app.logger.info(f"Redirecting user {current_user.email} with role {current_user.role}.")
    if current_user.has_role(UserRole.ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.DRIVER.value):
        return redirect(url_for('drivers.driver_dashboard'))
    elif current_user.has_role(UserRole.BODYGUARD.value):
        return redirect(url_for('bodyguards.bodyguard_dashboard'))
    elif current_user.has_role(UserRole.RESEARCHER.value):
        return redirect(url_for('researchers.researcher_dashboard'))
    elif current_user.has_role(UserRole.COORDINATOR.value):
        return redirect(url_for('coordinators.coordinator_dashboard'))
    elif current_user.has_role(UserRole.SECRETARY.value):
        return redirect(url_for('secretaries.secretary_dashboard'))
    elif current_user.has_role(UserRole.CHIEF_SECURITY_OFFICER.value):
        return redirect(url_for('chief_security_officers.chief_security_officer_dashboard'))
    elif current_user.has_role(UserRole.SUPER_ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.P_A.value):
        return redirect(url_for('personal_assistants.personal_assistant_dashboard'))
    else:
        return redirect(url_for('main.home'))
# create a route to view events
@events_bp.route('/view_events', methods=['GET', 'POST'], strict_slashes=False)
def view_events():
    """route to view events"""
    events = db_storage.all(Events)
    return render_template('events.html', events=events)



@events_bp.route('/delete_event/<int:event_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_event(event_id):
    """route to delete an event"""
    event = db_storage.get(Events, event_id)
    if event is None:
        return redirect(url_for('events.view_events'))
    db_storage.delete(event)
    db_storage.save()
    return redirect(url_for('events.view_events'))

@events_bp.route('/update_event/<int:event_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_event(event_id):
    """route to update an event"""
    event = db_storage.get(Events, event_id)
    if event is None:
        return redirect(url_for('events.view_events'))
    form = EventForm()
    if form.validate_on_submit():
        event_name = form.event_name.data
        event_description = form.event_description.data
        event_impact = form.event_impact.data
        event_owner = form.event_owner.data
        event_location = form.event_location.data
        event_contact = form.event_contact.data
        event.event_name = event_name
        event.event_description = event_description
        event.event_impact = event_impact
        event.event_owner = event_owner
        event.event_location = event_location
        event.event_contact = event_contact
        db_storage.save()
        return redirect(url_for('events.view_events'))
    return render_template('add_event.html', title='Update Event', form=form)