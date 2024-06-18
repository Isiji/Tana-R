#!/usr/bin/python3
"""Routes for the bills"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana import db_storage, bcrypt
from Tana.models.bills import Bills
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.models.legislationstages import LegislationStages
from Tana.bills.forms import BillForm

bills_bp = Blueprint('bills', __name__)

#create a route to add a bill using the form
@bills_bp.route('/add_bill', methods=['GET', 'POST'], strict_slashes=False)
def bills():
    form = BillForm()
    if form.validate_on_submit():
        bill = Bills(name=form.name.data, submitted_date=form.submitted_date.data, first_reading=form.first_reading.data, second_reading=form.second_reading.data, third_reading=form.third_reading.data, presidential_assent=form.presidential_assent.data, commencement=form.commencement.data, documents=form.documents.data)
        db_storage.new(bill)
        db_storage.save()
        flash('Bill has been added!', 'success')
        return redirect(url_for('bills.view_bills'))
    return render_template('bills.html', form=form)



#create a route to view the bills
@bills_bp.route('/view_bills', methods=['GET', 'POST'], strict_slashes=False)
def view_bills():
    bills = db_storage.all(Bills)
    return render_template('view_bills.html', bills=bills)