from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm
from Tana import db_storage
from datetime import datetime

reminders = Blueprint('reminders', __name__)

@reminders.route('/add_reminder', methods=['GET', 'POST'])
@login_required
def add_reminder():
    """Route for adding a reminder"""
    form = ReminderForm()
    
    if form.validate_on_submit():
        reminder_datetime = datetime.combine(form.reminder_date.data, form.reminder_time.data)
        if reminder_datetime <= datetime.now():
            flash('Reminder date and time must be in the future.', 'danger')
            return redirect(url_for('reminders.add_reminder'))
        
        reminder = Reminder(
            reminder_name=form.reminder_name.data,
            reminder_description=form.reminder_description.data,
            reminder_date=form.reminder_date.data,
            reminder_time=form.reminder_time.data,
            user_id=current_user.id
        )
        db_storage.new(reminder)
        db_storage.save()
        flash('Reminder set successfully', 'success')
        return redirect(url_for('reminders.add_reminder'))

    # Fetch all reminders for the current user
    user_reminders = db_storage.get_session().query(Reminder).filter_by(user_id=current_user.id).all()

    return render_template('reminders.html', title='Reminders', form=form, reminders=user_reminders)
