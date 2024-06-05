#!/usr/bin/python3
"""Routes for the reminders"""
from flask import Blueprint, jsonify, request
from flask import render_template, redirect, url_for, flash
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm, UpdateReminderForm, DeleteReminderForm, ReminderSearchForm
from Tana import db_storage, bcrypt


reminders = Blueprint('reminders', __name__)

#create a route for reminders template where on can set reminders
@reminders.route('/reminders', methods=['GET', 'POST'])
def reminders_page():
    """route for the reminders page"""
    form = ReminderForm()
    if form.validate_on_submit():
        reminder = Reminder(title=form.title.data, description=form.description.data, date=form.date.data, time=form.time.data)
        db_storage.new(reminder)
        db_storage.save()
        flash('Reminder set successfully', 'success')
        return redirect(url_for('reminders.reminders_page'))
    return render_template('reminders.html', title='Reminders', form=form)