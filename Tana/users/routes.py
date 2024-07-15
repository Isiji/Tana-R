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
from Tana.users.forms import DiaryForm, FileUploadForm
from Tana.models.pollingstation import PollingStation
from Tana.models.ward import Ward
from Tana.models.constituency import Constituency
from werkzeug.utils import secure_filename
from Tana.models.offices import Offices
import logging
from datetime import datetime, date
from Tana.models.diary import Diary
from flask_mail import Message
from Tana import mail, create_app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


#route for user registration

@Users.route('/register/<int:office_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def register(office_id):
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users.create_user(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            ID_No=form.ID_No.data,
            role=form.role.data,
            office_id=office_id
        )
        db_storage.new(user)
        db_storage.save()
        flash('User registered successfully.', 'success')
        return redirect(url_for('offices.office_details', office_id=office_id))
    return render_template('register.html', title='Register User', form=form)

@Users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#route for employee register using employee register form
@Users.route('/employee_register', methods=['GET', 'POST'])
@login_required
def employee_register():
    form = EmployeeRegisterForm()

    if request.method == 'GET':
        # Pre-fill the form with current user info
        form.user_id.data = current_user.id
        form.name.data = current_user.name
        form.date.data = datetime.now().date()
        form.time_in.data = datetime.now().strftime('%H:%M')

    if form.validate_on_submit():
        try:
            user_id = form.user_id.data
            name = form.name.data
            time_in = form.time_in.data
            date = form.date.data
            status = form.status.data

            # Create a new EmployeeRegister object
            new_employee = EmployeeRegister(
                user_id=user_id,
                name=name,
                time_in=time_in,  # No need to convert to datetime.time()
                date=date,
                status=status
            )
            
            # Add and commit the new employee to the database
            db_storage.new(new_employee)
            db_storage.save()

            flash('Employee registered successfully!', 'success')
            return redirect(url_for('Users.employee_records'))
        except Exception as e:
            logging.error(f"Error registering employee: {e}")
            flash('An error occurred while registering the employee. Please try again.', 'danger')

    return render_template('employee_register.html', title='Employee Register', form=form)

#route for getting all employee records
@Users.route('/employee_records', methods=['GET'])
@login_required
def employee_records():
    """Route to display employee records"""
    employees = db_storage.all(EmployeeRegister).values()  # Replace with your method to fetch employees
    return render_template('employee_records.html', title='Employee Records', employees=employees)


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
            return redirect(url_for('Users.login'))  # Redirect to login page if credentials are invalid

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
        return redirect(url_for('Users.admin_dashboard'))

    elif current_user.has_role(UserRole.FIELD_OFFICER.value):
        return redirect(url_for('fieldofficers.field_officers'))
    elif current_user.has_role(UserRole.CHIEF_FIELD_OFFICER.value):
        return redirect(url_for('chieffieldofficers.chieffieldofficer_dashboard'))
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
    
#route for the admin dashboard
@Users.route('/admin_dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    """Route for the admin dashboard"""
    if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value) or current_user.has_role(UserRole.P_A.value):
        if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.P_A.value):
            offices = db_storage.get_all_offices()
        else:
            # Assuming get_offices_for_user method is defined in DBStorage class
            offices = db_storage.get_offices_for_user(current_user.id)
        return render_template('admin_dashboard.html', title='Admin Dashboard', offices=offices)
    else:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main.home'))
    
#create a route for creating the diary
@Users.route('/create_diary', methods=['GET', 'POST'])
def create_diary():
    """route to create a diary"""
    form = DiaryForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        entry_date = form.entry_date.data

        diary = Diary(
            title=title,
            content=content,
            entry_date=entry_date,
            user_id=current_user.id
        )

        db_storage.new(diary)
        db_storage.save()

        flash('Diary created successfully!', 'success')
        return redirect(url_for('Users.view_diaries'))
    
    return render_template('create_diary.html', title='Create Diary', form=form)

#create a route to view diaries
#route to view diaries
@Users.route('/view_diaries', methods=['GET'])
def view_diaries():
    """route to view all diaries"""
    diaries = db_storage.all(Diary).values()
    return render_template('diary.html', title='View Diaries', diaries=diaries)

#route to delete a diary
@Users.route('/delete_diary/<int:diary_id>', methods=['GET', 'POST'])
def delete_diary(diary_id):
    """route to delete a diary"""
    diary = db_storage.get(Diary, diary_id)
    if diary is None:
        return redirect(url_for('Users.view_diaries'))
    db_storage.delete(diary)
    db_storage.save()
    return redirect(url_for('Users.view_diaries'))

#route to edit a diary
@Users.route('/edit_diary/<int:diary_id>', methods=['GET', 'POST'])
def edit_diary(diary_id):
    """Route to edit a diary entry"""
    diary = db_storage.get(Diary, id=diary_id)
    if not diary:
        flash('Diary not found', 'danger')
        return redirect(url_for('Users.view_diaries'))
    
    # Add logic for handling form submission to edit the diary
    if request.method == 'POST':
        # Update the diary fields here
        diary.title = request.form['title']
        diary.content = request.form['content']
        db_storage.save()
        flash('Diary updated successfully', 'success')
        return redirect(url_for('Users.view_diaries'))
    
    return render_template('edit_diary.html', title='Edit Diary', diary=diary)

#create route to reset password
@Users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """Route to reset user password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = users.get_user_by_email(form.email.data)
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account with that email. Please register first.', 'warning')
        return redirect(url_for('Users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@Users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Route to handle the reset token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = users.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db_storage.save()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

def send_reset_email(user):
    token = users.get_reset_token
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('Users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)