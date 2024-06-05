#!/usr/bin/python3
"""routes for the coordinators"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

coordinators = Blueprint('coordinators', __name__)

@coordinators.route('/coordinator_dashboard')
@login_required
def coordinator_dashboard():
    """route for the coordinator dashboard"""
    return render_template('coordinator.html', title='Coordinator Dashboard')