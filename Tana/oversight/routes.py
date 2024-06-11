#!/usr/bin/python3
"""Routes for the oversight"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana import db_storage, bcrypt
from Tana.models.oversight import Oversight
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.oversight.forms import OversightForm

oversight = Blueprint('oversight', __name__)

@oversight.route('/oversight_dashboard')
def oversight_dashboard():
    """route for the oversight dashboard"""
    return render_template('oversight.html', title='Oversight Dashboard')

# function for primary oversight
@oversight.route('/oversight_primary', methods=['GET', 'POST'])
def oversight_primary():
    """route for the primary oversight"""
    form = OversightForm()
    if form.validate_on_submit():
        oversight = Oversight(document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.session.add(oversight)
        db_storage.session.commit()
        flash('Oversight has been submitted', 'success')
        return redirect(url_for('oversight.oversight_primary'))
    return render_template('oversight.html', title='Primary Oversight', form=form)

# function for secondary oversight
@oversight.route('/oversight_secondary', methods=['GET', 'POST'])
def oversight_secondary():
    """route for the secondary oversight"""
    form = OversightForm()
    if form.validate_on_submit():
        oversight = Oversight(document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.session.add(oversight)
        db_storage.session.commit()
        flash('Oversight has been submitted', 'success')
        return redirect(url_for('oversight.oversight_secondary'))
    return render_template('oversight.html', title='Secondary Oversight', form=form)


