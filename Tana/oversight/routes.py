#!/usr/bin/python3
"""Routes for the oversight"""
from flask import Blueprint, render_template, send_file, request, redirect, url_for, flash
from Tana import db_storage, bcrypt
from Tana.models.secondaryoversight import SecondaryOversight
from flask_login import login_user, current_user, logout_user, login_required
from Tana.oversight.forms import OversightForm
import io

oversight_bp = Blueprint('oversight_bp', __name__)

@oversight_bp.route('/view_oversight')
@login_required
def view_oversight():
    """Route for viewing all oversight"""
    oversights = db_storage.all(SecondaryOversight).values()
    return render_template('view_oversight.html', title='View Oversight', oversights=oversights)

@oversight_bp.route('/edit_oversight/<int:oversight_id>', methods=['GET', 'POST'])
@login_required
def edit_oversight(oversight_id):
    """Route for editing secondary oversight"""
    oversight = db_storage.get(SecondaryOversight, id=oversight_id)
    if not oversight:
        flash(f'Oversight with ID {oversight_id} not found.', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))

    form = OversightForm()
    if form.validate_on_submit():
        oversight.OAG_Report = form.OAG_Report.data.read()
        oversight.date_updated = form.date_updated.data
        oversight.Ground_report = form.Ground_report.data
        oversight.status = form.status.data == 'Approved'
        db_storage.save()
        flash('Oversight has been updated', 'success')
        return redirect(url_for('oversight_bp.view_oversight'))

    # Prepopulate the form with existing data
    form.date_updated.data = oversight.date_updated
    form.Ground_report.data = oversight.Ground_report
    form.status.data = 'Approved' if oversight.status else 'Pending'

    return render_template('edit_oversight.html', title='Edit Oversight', form=form)

@oversight_bp.route('/delete_oversight/<int:oversight_id>', methods=['POST'])
@login_required
def delete_oversight(oversight_id):
    """Route for deleting secondary oversight"""
    oversight = db_storage.get(SecondaryOversight, id=oversight_id)
    if oversight:
        db_storage.delete(oversight)
        db_storage.save()
        flash('Oversight has been deleted', 'success')
    else:
        flash(f'Oversight with ID {oversight_id} not found.', 'error')
    return redirect(url_for('oversight_bp.view_oversight'))

@oversight_bp.route('/download_oversight/<int:oversight_id>')
@login_required
def download_oversight(oversight_id):
    """Route for downloading secondary oversight report"""
    oversight = db_storage.get(SecondaryOversight, id=oversight_id)
    if oversight:
        return send_file(
            io.BytesIO(oversight.OAG_Report),
            as_attachment=True,
            download_name=f'OAG_Report_{oversight_id}.pdf',
            mimetype='application/pdf'
        )
    else:
        flash(f'Oversight with ID {oversight_id} not found.', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))
