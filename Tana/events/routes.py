#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from Tana.models.eventcategory import EventCategory
from Tana.models.events import Events
from Tana import db_storage, bcrypt
from Tana.events.forms import EventForm, ViewEventForm

events_bp = Blueprint('events', __name__)

# create a route to add events
@events_bp.route('/add_event', methods=['GET', 'POST'], strict_slashes=False)
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
        return redirect(url_for('events.add_event'))

    return render_template('add_event.html', title='Add Event', form=form)

# create a route to view events
@events_bp.route('/view_events', methods=['GET', 'POST'], strict_slashes=False)
def view_events():
    """route to view events"""
    form = ViewEventForm()
    if form.validate_on_submit():
        events = db_storage.all(Events)
        return render_template('view_events.html', title='View Events', events=events)
    return render_template('events.html', title='View Events', form=form)

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