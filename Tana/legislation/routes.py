#!/usr/bin/python3
"""Routes for the legislation"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

legislation_bp = Blueprint('legislation', __name__)

@legislation_bp.route('/legislation')
def legislation():
    """route for the legislation"""
    return render_template('legislation.html', title='Legislation')
