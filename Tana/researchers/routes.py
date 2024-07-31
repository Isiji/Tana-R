from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.committees import Committee
from Tana.models.committee_records import CommitteeRecord
from Tana import db_storage
from Tana.researchers.forms import CommitteeForm, CommitteeRecordForm
from flask_login import login_required, current_user
from flask import send_file
from io import BytesIO


researchers = Blueprint('researchers', __name__)

@researchers.route('/researcher_dashboard')
@login_required
def researcher_dashboard():
    researchers = db_storage.get_researchers()
    return render_template('researcher.html', researchers=researchers)

@researchers.route('/committees', methods=['GET', 'POST'])
@login_required
def committees():
    form = CommitteeForm()
    if form.validate_on_submit():
        committee = Committee(name=form.name.data)
        db_storage.new(committee)
        db_storage.save()
        flash('Committee added successfully!', 'success')
        return redirect(url_for('researchers.committees'))

    committees = db_storage.all(Committee)
    return render_template('committees.html', title='Committees', form=form, committees=committees)

@researchers.route('/committee/<int:committee_id>', methods=['GET', 'POST'])
@login_required
def committee(committee_id):
    committee = db_storage.get(Committee, committee_id)
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
        return redirect(url_for('researchers.committee', committee_id=committee_id))

    records = db_storage.filter(CommitteeRecord, CommitteeRecord.committee_id == committee_id)
    return render_template('committee.html', committee=committee, records=records, form=form)

@researchers.route('/download_document/<int:record_id>')
@login_required
def download_document(record_id):
    record = db_storage.get(CommitteeRecord, record_id)
    if record and record.document:
        return send_file(BytesIO(record.document), as_attachment=True, attachment_filename='document.pdf')
    flash('Document not found.', 'danger')
    return redirect(url_for('researchers.committee', committee_id=record.committee_id))

@researchers.route('/download_recommendations/<int:record_id>')
@login_required
def download_recommendations(record_id):
    record = db_storage.get(CommitteeRecord, record_id)
    if record and record.recommendations:
        return send_file(BytesIO(record.recommendations), as_attachment=True, attachment_filename='recommendations.pdf')
    flash('Recommendations not found.', 'danger')
    return redirect(url_for('researchers.committee', committee_id=record.committee_id))