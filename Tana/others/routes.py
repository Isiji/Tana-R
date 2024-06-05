#!/usr/bin/python3
"""routes for the others"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

others = Blueprint('others', __name__)

@others.route('/others_dashboard')
@login_required
def others_dashboard():
    """route for the others dashboard"""
    return render_template('others.html', title='Others Dashboard')