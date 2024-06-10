#!/usr/bin/python3
"""routes for the representation"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

representation = Blueprint('representation', __name__)

@representation.route('/representation', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def representation_dashboard():
    """route for the representation dashboard"""
    return render_template('representation.html', title='representation Dashboard')