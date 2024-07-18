#!/usr/bin/python3
"""Routes for the reminders"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm
from Tana import db_storage

reminders = Blueprint('reminders', __name__)

@reminders.route('/add_reminder', methods=['GET', 'POST'])
def add_reminder():
    """Route for the reminders page"""
    form = ReminderForm()
    if form.validate_on_submit():
        reminder = Reminder(
            reminder_name=form.reminder_name.data,
            reminder_description=form.reminder_description.data,
            reminder_date=form.reminder_date.data,
            reminder_time=form.reminder_time.data,
            reminder_location=form.reminder_location.data,
            reminder_contact=form.reminder_contact.data
        )
        db_storage.new(reminder)
        db_storage.save()
        flash('Reminder set successfully', 'success')
        return redirect(url_for('reminders.reminders_page'))

    reminders = db_storage.all(Reminder).values()
    return render_template('reminders.html', title='Reminders', form=form, reminders=reminders)
