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

legislation_bp = Blueprint('legislation', __name__)

@legislation_bp.route('/legislation')
def legislation():
    """route for the legislation"""
    return render_template('legislation.html', title='Legislation')

#route for adding a motion using addmotion form
@legislation_bp.route('/add_motion', methods=['GET', 'POST'])
def add_motion():
    """route for the motions"""
    form = AddMotionForm()
    if form.validate_on_submit():
        motion = Motions(name=form.name.data, document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.save(motion)
        flash('Motion has been created!', 'success')
        return redirect(url_for('legislation.add_motion'))
    return render_template('add_motion.html', title='Add Motion', form=form)

@legislation_bp.route('/motions', methods=['GET', 'POST'])
def motions():
    """route for the motions"""
    return render_template('motions.html', title='Motions')


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
def questions():
    """route for the questions"""
    return render_template('questions.html', title='Questions')

@legislation_bp.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """route for the questions"""
    form = QuestionsForm()
    if form.validate_on_submit():
        question = Questions(name=form.name.data, document=form.document.data, date=form.date.data, status=form.status.data)
        db_storage.save(question)
        flash('Question has been created!', 'success')
        return redirect(url_for('legislation.add_question'))
    return render_template('add_question.html', title='Add Question', form=form)