#!/usr/bin/python3
"""Routes for the legislation"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.models.motions import Motions
from Tana.models.questions import Questions
from Tana.models.statements import Statements
from Tana.legislation.forms import MotionsForm, StatementsForm, LegislationForm, AddMotionForm, QuestionsForm
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


legislation_bp = Blueprint('legislation', __name__)

@legislation_bp.route('/legislation')
def legislation():
    """route for the legislation"""
    return render_template('legislation.html', title='Legislation')

#route for adding a motion using addmotion form
@legislation_bp.route('/add_motion', methods=['GET', 'POST'])
def add_motion():
    """Route for adding motions"""
    print('add motion route has been hit')
    form = MotionsForm()
    print('form created')
    if form.validate_on_submit():
        motion = Motions(
            name=form.name.data,
            document=form.document.data.read(),  # Read the file data
            date=form.date.data,
            status=form.status.data
        )
        try:
            db_storage.new(motion)
            db_storage.save()
            flash('Motion has been created!', 'success')
            logger.info(f"Motion '{motion.name}' added to the database.")
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f"Failed to add motion '{form.name.data}' to the database. Error: {str(e)}")
        return redirect(url_for('legislation.add_motion'))
    return render_template('add_motion.html', title='Add Motion', form=form)
@legislation_bp.route('/motions', methods=['GET'])
def motions():
    motions_dict = db_storage.all(Motions)
    motions = list(motions_dict.values())
    return render_template('motions.html', title='View Motions', motions=motions)
@legislation_bp.route('/edit_motion/<int:motion_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_motion(motion_id):
    motion = db_storage.get(Motions, id=motion_id)
    form = MotionsForm(obj=motion)
    if form.validate_on_submit():
        try:
            motion.name = form.name.data
            motion.date = form.date.data
            motion.status = form.status.data
            if form.document.data:
                motion.document = form.document.data.read()
            db_storage.save()
            flash('Motion has been updated!', 'success')
            return redirect(url_for('legislation.view_motions'))
        except Exception as e:
            logging.error(f"Error editing motion: {e}")
            flash('An error occurred while editing the motion. Please try again.', 'danger')
    return render_template('edit_motion.html', title='Edit Motion', form=form, motion=motion)

@legislation_bp.route('/delete_motion/<int:motion_id>', methods=['POST'], strict_slashes=False)
def delete_motion(motion_id):
    motion = db_storage.get(Motions, id=motion_id)
    db_storage.delete(motion)
    db_storage.save()
    flash('Motion has been deleted!', 'success')
    return redirect(url_for('legislation.motions'))

@legislation_bp.route('/statements', methods=['GET', 'POST'])
def statements():
    """route for the statements"""
    return render_template('statements.html', title='Statements')

@legislation_bp.route('/add_statement', methods=['GET', 'POST'])
def add_statement():
    """route for the statements"""
    form = StatementsForm()
    if form.validate_on_submit():
        statement = Statements(name=form.name.data, document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.save(statement)
        flash('Statement has been created!', 'success')
        return redirect(url_for('legislation.add_statement'))
    return render_template('add_statement.html', title='Add Statement', form=form)

@legislation_bp.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    """route for the questions"""
    return render_template('questions.html', title='Questions')

@legislation_bp.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    """route for the questions"""
    form = QuestionsForm()
    if form.validate_on_submit():
        question = Questions(name=form.name.data, document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.new(question)
        db_storage.save()
        flash('Question has been created!', 'success')
        return redirect(url_for('legislation.add_question'))
    return render_template('add_question.html', title='Add Question', form=form)

#create a route for functions
@legislation_bp.route('/functions', methods=['GET', 'POST'])
def functions():
    """route for the functions"""
    return render_template('functions.html', title='Functions')