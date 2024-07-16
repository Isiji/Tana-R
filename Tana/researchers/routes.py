#!/usr/bin/python3
"""Routes for the researchers"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

researchers = Blueprint('researchers', __name__)

@researchers.route('/researcher_dashboard')
@login_required
def researcher_dashboard():
    researchers = db_storage.get_researchers()
    return render_template('researcher.html', researchers=researchers)
