#!/usr/bin/python3
"""Bills routes"""
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_required
from Tana import db_storage
from Tana.models.bills import Bills
from Tana.bills.forms import BillsForm
import logging

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('/add_bill', methods=['GET', 'POST'], strict_slashes=False)
def add_bill():
    form = BillsForm()
    if form.validate_on_submit():
        try:
            bill = Bills(
                name=form.bill_name.data,
                submitted_date=form.submitted_date.data,
                first_reading=form.first_reading.data,
                second_reading=form.second_reading.data,
                third_reading=form.third_reading.data,
                presidential_assent=form.presidential_assent.data,
                commencement=form.commencement.data
            )
            db_storage.new(bill)
            db_storage.save()
            flash('Bill has been added!', 'success')
            return redirect(url_for('bills.view_bills'))
        except Exception as e:
            logging.error(f"Error adding bill: {e}")
            flash('An error occurred while adding the bill. Please try again.', 'danger')
    return render_template('add_bill.html', form=form)

#route to view bills
@bills_bp.route('/view_bills', methods=['GET'], strict_slashes=False)
def view_bills():
    bills = db_storage.all(Bills)
    print(bills)  # Debug: Check the content of bills
    return render_template('view_bills.html', bills=bills)


@bills_bp.route('/view_bill/<int:bill_id>', methods=['GET'], strict_slashes=False)
def view_bill(bill_id):
    bill = db_storage.get(Bills, bill_id)
    return render_template('view_bill.html', bill=bill)

@bills_bp.route('/edit_bill/<int:bill_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_bill(bill_id):
    bill = db_storage.get(Bills, bill_id)
    form = BillsForm(obj=bill)
    if form.validate_on_submit():
        form.populate_obj(bill)
        db_storage.save()
        flash('Bill has been updated!', 'success')
        return redirect(url_for('bills.view_bills'))
    return render_template('edit_bill.html', form=form, bill=bill)

@bills_bp.route('/delete_bill/<int:bill_id>', methods=['POST'], strict_slashes=False)
def delete_bill(bill_id):
    bill = db_storage.get(Bills, bill_id)
    db_storage.delete(bill)
    db_storage.save()
    flash('Bill has been deleted!', 'success')
    return redirect(url_for('bills.view_bills'))