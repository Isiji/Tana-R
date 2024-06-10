#!/usr/bin/python3
"""routes for the lobbying"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

lobbying = Blueprint('lobbying', __name__)

@lobbying.route('/lobbying_dashboard')
@login_required
def lobbying_dashboard():
    """route for the lobbying dashboard"""
    return render_template('lobbying.html', title='lobbying Dashboard')