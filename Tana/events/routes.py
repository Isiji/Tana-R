#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from Tana.models.funcategory import FunctionCategory
from Tana.models.events import Events
from Tana import db_storage, bcrypt
from Tana.events.forms import EventForm

events = Blueprint('events', __name__)

# create a route to add events
@events.route('/add_event', methods=['GET', 'POST'], strict_slashes=False)
def add_event():
    """route to add an event"""
    form = EventForm()
    if form.validate_on_submit():
        function_name = form.function_name.data
        function_description = form.function_description.data
        function_impact = form.function_impact.data
        function_owner = form.function_owner.data
        function_location = form.function_location.data
        function_contact = form.function_contact.data
        event = events(function_name=function_name, function_description=function_description, function_impact=function_impact, function_owner=function_owner, function_location=function_location, function_contact=function_contact)
        db_storage.new(event)
        db_storage.save()
        return redirect(url_for('events.add_event'))
    return render_template('add_event.html', title='Add Event', form=form)

# create a route to view events
@events.route('/view_events', methods=['GET', 'POST'], strict_slashes=False)
def view_events():
    """route to view events"""
    events = db_storage.all(events)
    return render_template('view_events.html', title='View Events', events=events)