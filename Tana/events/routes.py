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
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation

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

        polling_station_name = form.polling_station_name.data

        polling_station = db_storage.find_one(PollingStation, name=polling_station_name)

        if not polling_station:
            flash('Polling station not found!', 'danger')
            return redirect(url_for('events.add_event'))

        event = Events(
            event_name=event_name, 
            event_description=event_description, 
            impact_level=impact_level, 
            event_owner=event_owner, 
            event_location=event_location, 
            event_contact=event_contact,
            event_date=event_date,
            polling_station_id=polling_station.id
        )

        db_storage.new(event)
        db_storage.save()
        flash('Event has been created!', 'success')
        return redirect(url_for('events.view_events'))

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



@events_bp.route('/get_all_polling_stations', methods=['GET'])
def get_all_polling_stations():
    """Route to get all polling station names"""
    polling_stations = db_storage.all(PollingStation)
    polling_station_names = [station.name for station in polling_stations.values()]
    return jsonify({'pollingStations': polling_station_names})

@events_bp.route('/get_polling_station_info', methods=['GET'])
def get_polling_station_info():
    polling_station_name = request.args.get('polling_station')

    if not polling_station_name:
        return jsonify({'error': 'Polling station name is required'}), 400

    polling_station = db_storage.find_one(PollingStation, name=polling_station_name)

    if not polling_station:
        return jsonify({'error': 'Polling station not found'}), 404

    ward = db_storage.find_one(Ward, id=polling_station.ward_id)
    constituency = db_storage.find_one(Constituency, id=ward.constituency_id)

    return jsonify({
        'ward': ward.name,
        'constituency': constituency.name
    })