# routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm
from Tana import db_storage

reminders = Blueprint('reminders', __name__)

@reminders.route('/add_reminder', methods=['GET', 'POST'])
@login_required
def add_reminder():
    """Route for adding a reminder"""
    form = ReminderForm()
    if form.validate_on_submit():
        reminder = Reminder(
            reminder_name=form.reminder_name.data,
            reminder_description=form.reminder_description.data,
            reminder_date=form.reminder_date.data,
            reminder_time=form.reminder_time.data,
            user_id=current_user.id  # Assign current user's ID to the reminder
        )
        db_storage.new(reminder)
        db_storage.save()
        flash('Reminder set successfully', 'success')
        return redirect(url_for('reminders.reminders_page'))

    return render_template('reminders.html', title='Add Reminder', form=form)

@reminders.route('/view_reminders')
@login_required
def view_reminders():
    """Route for viewing reminders"""
    reminders = db_storage.all(Reminder, filters={'user_id': current_user.id}, order_by={'reminder_date': 'desc', 'reminder_time': 'desc'})
    return render_template('reminders.html', title='Reminders', reminders=reminders)
