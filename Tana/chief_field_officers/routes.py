#!/usr/bin/python3
"""routes for the chief field officers"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

chieffieldofficers = Blueprint('chieffieldofficers', __name__)

@chieffieldofficers.route('/chieffieldofficer_dashboard')
@login_required
def chieffieldofficer_dashboard():
    """route for the chief field officer dashboard"""
    return render_template('chieffieldofficer.html', title='Chief Field Officer Dashboard')