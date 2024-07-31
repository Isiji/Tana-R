#!/usr/bin/python3
"""Routes for the oversight"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from Tana import db_storage
from Tana.models.secondaryoversight import SecondaryOversight
from Tana.oversight.forms import OversightForm
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
import logging
from io import BytesIO
from werkzeug.utils import secure_filename

oversight_bp = Blueprint('oversight_bp', __name__)

@oversight_bp.route('/view_oversight', methods=['GET'], strict_slashes=False)
def view_oversight():
    oversights_dict = db_storage.all(SecondaryOversight)
    oversights = list(oversights_dict.values())
    return render_template('view_oversight.html', title='View Oversight', oversights=oversights)

@oversight_bp.route('/add_oversight', methods=['GET', 'POST'])
@login_required
def add_oversight():
    """route for adding secondary oversight"""
    form = OversightForm()
    if form.validate_on_submit():
        OAG_Report = form.OAG_Report.data.read()
        date_updated = form.date_updated.data
        Ground_report = form.Ground_report.data
        status = form.status.data == 'Approved'
        oversight = SecondaryOversight(OAG_Report=OAG_Report, date_updated=date_updated, Ground_report=Ground_report, status=status)
        db_storage.new(oversight)
        db_storage.save()
        flash('Oversight has been submitted', 'success')
        return redirect(url_for('oversight_bp.view_oversight'))
    return render_template('oversight_form.html', title='Add Oversight', form=form)



@oversight_bp.route('/edit_oversight/<int:oversight_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_oversight(oversight_id):
    oversight = db_storage.get(SecondaryOversight, id=oversight_id)
    if not oversight:
        flash(f'Oversight with ID {oversight_id} not found.', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))

    form = OversightForm(obj=oversight)
    if form.validate_on_submit():
        try:
            # Only update the document if a new file is uploaded
            if form.document.data:
                oversight.document = form.document.data.read()
                oversight.document_filename = secure_filename(form.document.data.filename)

            # Update other fields
            oversight.name = form.name.data
            oversight.description = form.description.data
            oversight.date = form.date.data
            # Add any other oversight attributes here as necessary
            
            db_storage.save()
            flash('Oversight has been updated!', 'success')
            return redirect(url_for('oversight_bp.view_oversight'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('edit_oversight.html', title='Edit Oversight', form=form, oversight=oversight)

@oversight_bp.route('/delete_oversight/<int:oversight_id>', methods=['POST'], strict_slashes=False)
def delete_oversight(oversight_id):
    oversight = db_storage.get(SecondaryOversight, oversight_id)
    db_storage.delete(oversight)
    db_storage.save()
    flash('Oversight has been deleted!', 'success')
    return redirect(url_for('oversight_bp.view_oversight'))

@oversight_bp.route('/download_oversight/<int:oversight_id>', methods=['GET'])
def download_oversight(oversight_id):
    """Route to download an oversight document."""
    try:
        oversight = db_storage.get(SecondaryOversight, id=oversight_id)
        if not oversight:
            flash(f'Oversight with ID {oversight_id} not found.', 'error')
            return redirect(url_for('oversight_bp.view_oversight'))

        return send_file(BytesIO(oversight.document), as_attachment=True, download_name=oversight.document_filename)

    except Exception as e:
        flash(f'An error occurred while downloading the oversight document: {e}', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))