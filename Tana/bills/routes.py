#!/usr/bin/python3
"""Bills routes"""
from flask import render_template, flash, redirect, url_for, request, Blueprint
from Tana import db_storage
from Tana.models.bills import Bills
from Tana.bills.forms import BillsForm
import logging
from io import BytesIO
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

bills_bp = Blueprint('bills', __name__)


@bills_bp.route('/add_bill', methods=['GET', 'POST'], strict_slashes=False)
def add_bill():
    form = BillsForm()
    if form.validate_on_submit():
        try:
            document_data = form.document.data.read()
            document_filename = secure_filename(form.document.data.filename)
            
            bill = Bills(
                name=form.bill_name.data,
                submitted_date=form.submitted_date.data,
                first_reading=form.first_reading.data,
                second_reading=form.second_reading.data,
                third_reading=form.third_reading.data,
                presidential_assent=form.presidential_assent.data,
                commencement=form.commencement.data,
                document=document_data,
                filename=document_filename
            )
            db_storage.new(bill)
            db_storage.save()  # Ensure the session is committed
            flash('Bill has been added!', 'success')
            return redirect(url_for('bills.view_bills'))
        except Exception as e:
            db_storage.rollback()
            logging.error(f"Error adding bill: {e}")
            flash('An error occurred while adding the bill. Please try again.', 'danger')
    return render_template('add_bill.html', form=form)


@bills_bp.route('/view_bills', methods=['GET'], strict_slashes=False)
def view_bills():
    bills_dict = db_storage.all(Bills)
    bills = list(bills_dict.values())
    return render_template('view_bills.html', bills=bills)

@bills_bp.route('/edit_bill/<int:bill_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_bill(bill_id):
    bill = db_storage.get(Bills, id=bill_id)
    if not bill:
        flash(f'Bill with id {bill_id} not found.', 'error')
        return redirect(url_for('bills.view_bills'))  # Redirect to a meaningful page

    form = BillsForm(obj=bill)
    if form.validate_on_submit():
        form.populate_obj(bill)
        if form.document.data:  # Only update the content if a new file is uploaded
            bill.document = form.document.data.read()
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


@bills_bp.route('/download_bill/<int:bill_id>', methods=['GET'])
def download_bill(bill_id):
    """Route to download a bill."""
    try:
        bill = db_storage.get(Bills, id=bill_id)
        if not bill:
            flash(f'Bill with ID {bill_id} not found.', 'error')
            return redirect(url_for('bills.view_bills'))

        return send_file(BytesIO(bill.document), as_attachment=True, download_name=bill.filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the bill: {e}', 'error')
        return redirect(url_for('bills.view_bills'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the bill: {e}', 'error')
        return redirect(url_for('bills.view_bills'))