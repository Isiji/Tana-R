from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from io import BytesIO
from Tana.models.committee_records import CommitteeRecord
from Tana.researchers.forms import CommitteeRecordForm
from Tana import db_storage

# Define the blueprint
researchers = Blueprint('researchers', __name__)

# Hardcoded list of committees
COMMITTEES = [
    {'id': 1, 'name': 'Energy Committee'},
    {'id': 2, 'name': 'Delegated Legislation Committee'},
    {'id': 3, 'name': 'Pan African Parliament Committee'},
    {'id': 4, 'name': 'Bunge Sports Club'},
    {'id': 5, 'name': 'CPAC'},
    {'id': 6, 'name': 'CPIC'},
]

@researchers.route('/committees', methods=['GET'])
@login_required
def committees():
    form = CommitteeRecordForm()
    return render_template('committees.html', title='Committees', form=form, committees=COMMITTEES)

@researchers.route('/committee/<int:committee_id>', methods=['GET', 'POST'])
@login_required
def committee(committee_id):
    # Find committee by ID
    committee = next((c for c in COMMITTEES if c['id'] == committee_id), None)
    if not committee:
        flash('Committee not found.', 'danger')
        return redirect(url_for('researchers.committees'))

    form = CommitteeRecordForm()
    if form.validate_on_submit():
        document = form.document.data.read() if form.document.data else None
        recommendations = form.recommendations.data.read() if form.recommendations.data else None
        record = CommitteeRecord(
            serial_number=form.serial_number.data,
            date=form.date.data,
            title=form.title.data,
            document=document,
            recommendations=recommendations,
            committee_id=committee_id
        )
        db_storage.new(record)
        db_storage.save()
        flash('Record added successfully!', 'success')
        return redirect(url_for('researchers.committee_records', committee_id=committee_id))

    records = db_storage.filter(CommitteeRecord, CommitteeRecord.committee_id == committee_id)
    return render_template('committee.html', committee=committee, records=records, form=form)

@researchers.route('/committee/<int:committee_id>/records', methods=['GET'])
@login_required
def committee_records(committee_id):
    records = db_storage.filter(CommitteeRecord, CommitteeRecord.committee_id == committee_id)
    return render_template('committee_records.html', records=records, committee_id=committee_id)

@researchers.route('/download_document/<int:record_id>')
@login_required
def download_document(record_id):
    record = db_storage.get(CommitteeRecord, record_id)
    if record and record.document:
        return send_file(BytesIO(record.document), as_attachment=True, attachment_filename='document.pdf')
    flash('Document not found.', 'danger')
    return redirect(url_for('researchers.committee_records', committee_id=record.committee_id))

@researchers.route('/download_recommendations/<int:record_id>')
@login_required
def download_recommendations(record_id):
    record = db_storage.get(CommitteeRecord, record_id)
    if record and record.recommendations:
        return send_file(BytesIO(record.recommendations), as_attachment=True, attachment_filename='recommendations.pdf')
    flash('Recommendations not found.', 'danger')
    return redirect(url_for('researchers.committee_records', committee_id=record.committee_id))
