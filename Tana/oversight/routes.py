#!/usr/bin/python3
"""Routes for the oversight"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

oversight = Blueprint('oversight', __name__)

@oversight.route('/oversight_dashboard')
@login_required
def oversight_dashboard():
    """route for the oversight dashboard"""
    return render_template('oversight.html', title='Oversight Dashboard')