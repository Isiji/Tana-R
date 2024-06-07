#!/usr/bin/python3
"""main class for the module"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.main.forms import loginForm
from flask import session

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')


#create a unified login route for both users and offices
@main.route('/login', methods=['GET', 'POST'])
def login():
    """login route for the user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = loginForm()

    if form.validate_on_submit():
        
        user_data = {}
        for model_class in [users, Offices]:
            user_data.update(db_storage.all(model_class))
        for appuser in user_data.values():
            if appuser.email == form.email.data and bcrypt.check_password_hash(appuser.password, form.password.data):
                session['email'] = form.email.data
                session['password'] = form.password.data
                session['user_id'] = appuser.id
                
                login_user(appuser, remember=form.remember.data)
                
                if isinstance(appuser, Offices):
                    return redirect(url_for('offices.office_dashboard'))
                
                elif appuser.role == 'super_admin':
                    return redirect(url_for('Users.admin_dashboard'))
                elif appuser.role == 'admin':
                    return redirect(url_for('offices.admin_dashboard'))
                elif appuser.role == 'driver':
                    return redirect(url_for('drivers.driver_dashboard'))
                elif appuser.role == 'manager':
                    return redirect(url_for('managers.manager_dashboard'))
                elif appuser.role == 'bodyguard':
                    return redirect(url_for('bodyguards.bodyguard_dashboard'))
                elif appuser.role == 'reseacher':
                    return redirect(url_for('reseachers.reseacher_dashboard'))
                elif appuser.role == 'secretary':
                    return redirect(url_for('secretaries.secretary_dashboard'))
                elif appuser.role == 'chief_field_officer':
                    return redirect(url_for('chieffieldofficers.chieffieldofficer_dashboard'))
                elif appuser.role == 'chief_security_officer':
                    return redirect(url_for('chiefsecurityofficers.chiefsecurityofficer_dashboard'))
                elif appuser.role == 'cordinator':
                    return redirect(url_for('cordinators.cordinator_dashboard'))
                elif appuser.role == 'field_officer':
                    return redirect(url_for('fieldofficers.fieldofficer_dashboard'))
                elif appuser.role == 'other':
                    return redirect(url_for('others.other_dashboard'))
                else:
                    return redirect(url_for('main.home'))
                
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    """logout route for the user"""
    logout_user()
    return redirect(url_for('main.home'))
