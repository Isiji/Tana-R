#!/usr/bin/env python3
"""Users route for the users"""
import os
from flask import Blueprint, session, jsonify, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana.engine.storage import DBStorage
from Tana.users.forms import UpdateAccountForm, RequestResetForm, LoginForm,ResetPasswordForm, RegistrationForm, EmployeeRegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from Tana import bcrypt, db_storage, allowed_file
from Tana.models.employee_register import EmployeeRegister
from Tana.users.forms import FileUploadForm
from Tana.models.pollingstation import PollingStation
from Tana.models.ward import Ward
from Tana.models.constituency import Constituency
from werkzeug.utils import secure_filename
from Tana.models.offices import Offices

Users = Blueprint('Users', __name__)

# create a route for homepage
@Users.route('/')
@Users.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')

# create route for user to update user information
@Users.route('/account', methods=['GET', 'POST'])
def account():
    """account route for the user"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        db_storage = DBStorage()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db_storage.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

#create route for admin dashboard
@Users.route('/admin_dashboard', methods=['POST', 'GET'], strict_slashes=False)
def admin_dashboard():
    """route for the admin dashboard"""
    if current_user.is_authenticated:
        if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value):
            return render_template('admin_dashboard.html', title='Admin Dashboard')
        else:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.home'))
    else:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('Users.login'))

#route for user registration

@Users.route('/register', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        print("Form validated successfully")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        if current_user.has_role('SUPER_ADMIN') or current_user.has_role('P_A'):
            office_id = form.office_id.data
        elif current_user.has_role('ADMIN'):
            office_id = current_user.office_id
        else:
            office_id = None  # Ensure office_id is set to a valid value

        try:
            new_user_role = form.role.data
            if new_user_role not in UserRole._value2member_map_:
                raise ValueError("Invalid role")

            user = users.create_user(
                name=form.name.data,
                email=form.email.data,
                password=hashed_password,
                phone=form.phone.data,
                ID_No=form.ID_No.data,
                role=new_user_role,
                office_id=office_id
            )
            
            db_storage.new(user)
            db_storage.save()
            print("User saved successfully")
            flash('User registered successfully.', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            print(f"Error registering user: {e}")
            flash('Error registering user.', 'danger')
    
    return render_template('register.html', title='Register User', form=form)

@Users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#route for employee register using employee register form
@Users.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
    """route for the employee register"""
    form = EmployeeRegisterForm()
    if form.validate_on_submit():
        employee = EmployeeRegister(name=form.name.data, time_in=form.time_in.data, time_out=form.time_out.data, date=form.date.data, status=form.status.data)
        db_storage.save(employee)
        flash('Registered!', 'success')
        return redirect(url_for('Users.redirect_based_on_role'))
    return render_template('employee_register.html', title='Employee Register', form=form)


@Users.route('/upload', methods=['GET', 'POST'])
def upload():
    form = FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Process the file and populate database
            flash('File uploaded successfully', 'success')
            return redirect(url_for('Users.upload'))
        else:
            flash('Invalid file type', 'danger')
    return render_template('upload.html', form=form)

@Users.route('/search', methods=['GET'])
def search():
    polling_station_name = request.args.get('polling_station')
    polling_station = PollingStation.query.filter_by(name=polling_station_name).first()
    if polling_station:
        ward = polling_station.ward
        constituency = ward.constituency
        return jsonify({'ward': ward.name, 'constituency': constituency.name})
    return jsonify({'error': 'Polling station not found'}), 404

@Users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Users.redirect_based_on_role'))  # Redirect to role-based redirect after login

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db_storage.get_user_by_email(email)

        if user is None or not bcrypt.check_password_hash(user.password, password):
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('login'))  # Redirect to login page if credentials are invalid

        login_user(user, remember=form.remember.data)

        session['user_id'] = user.id
        session['role'] = user.role
        session['email'] = user.email

        return redirect(url_for('Users.redirect_based_on_role'))  # Redirect to role-based redirection

    # If form is not submitted or validation fails, render login template
    print("current user is not authenticated")
    all_users = db_storage.all(users)
    print("All users:", all_users)
    print("Form is valid:", form.validate_on_submit())
    print("Form errors:", form.errors)
    print("Form data:", form.data)
    
    return render_template('login.html', title='Login', form=form)


@Users.route('/redirect_based_on_role', methods=['GET', 'POST'])
@login_required
def redirect_based_on_role():
    """Route to redirect based on the user role"""
    current_app.logger.info(f"Redirecting user {current_user.email} with role {current_user.role}.")
    print(f"Redirecting user {current_user.email} with role {current_user.role}.")
    if current_user.has_role(UserRole.ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.DRIVER.value):
        return redirect(url_for('drivers.driver_dashboard'))
    elif current_user.has_role(UserRole.BODYGUARD.value):
        return redirect(url_for('bodyguards.bodyguard_dashboard'))
    elif current_user.has_role(UserRole.RESEARCHER.value):
        return redirect(url_for('researchers.researcher_dashboard'))
    elif current_user.has_role(UserRole.COORDINATOR.value):
        return redirect(url_for('coordinators.coordinator_dashboard'))
    elif current_user.has_role(UserRole.SECRETARY.value):
        return redirect(url_for('secretaries.secretary_dashboard'))
    elif current_user.has_role(UserRole.CHIEF_SECURITY_OFFICER.value):
        return redirect(url_for('chief_security_officers.chief_security_officer_dashboard'))
    elif current_user.has_role(UserRole.SUPER_ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.P_A.value):
        return redirect(url_for('personal_assistants.personal_assistant_dashboard'))
    else:
        return redirect(url_for('main.home'))


#create a route for the admin page, admins include P.A, Super Admin, Admin
@Users.route('/admin', methods=['GET', 'POST'])
def admin():
    """route for the admin page"""
    if current_user.is_authenticated:
        if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value):
            return render_template('admin.html', title='Admin')
        else:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.home'))
    else:
        flash('You need to be logged in to access this page', 'danger')
        return redirect(url_for('Users.login'))
    
