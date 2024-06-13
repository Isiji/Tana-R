#!/usr/bin/python3
"""Routes for the bills"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana import db_storage, bcrypt
from Tana.models.bills import Bills
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.models.legislationstages import LegislationStages

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('/add_bill', methods=['GET', 'POST'], strict_slashes=False)
def add_bill():
    """route for the bills"""
    if request.method == 'POST':
        bill_name = request.form['bill_name']
        submitted_date = request.form['submitted_date']
        first_reading = 'first_reading' in request.form
        second_reading = 'second_reading' in request.form
        third_reading = 'third_reading' in request.form
        presidential_assent = 'presidential_assent' in request.form
        commencement = 'commencement' in request.form
        document = request.files['document']
        
        document_path = f"documents/{bill_name}.pdf"
        document.save(document_path)
        
        bill = Bills(name=bill_name, submitted_date=submitted_date, first_reading=first_reading,
                     second_reading=second_reading, third_reading=third_reading, presidential_assent=presidential_assent,
                     commencement=commencement)
        
        db_storage.new(bill)
        db_storage.save()
        
        flash('Bill created successfully', 'success')
        
        legislationstage = LegislationStages(stage="First Reading", bill_id=bill.id, document_path=document_path)
        db_storage.new(legislationstage)
        db_storage.save()
        
        return redirect(url_for('bills.bills'))
    
    return render_template('bills.html', title='Bills')


