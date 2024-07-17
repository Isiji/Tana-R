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
from datetime import datetime
from io import BytesIO
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError

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
            status=form.status.data,
            created_at=datetime.utcnow()
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
        return redirect(url_for('legislation.motions'))
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

#route for viewing motions
@legislation_bp.route('/view_motions', methods=['GET'])
def view_motions():
    motions_dict = db_storage.all(Motions)
    motions = list(motions_dict.values())
    return render_template('motions.html', title='View Motions', motions=motions)

@legislation_bp.route('/statements', methods=['GET', 'POST'])
def statements():
    """route for the statements"""
    return render_template('view_statements.html', title='Statements')

@legislation_bp.route('/add_statement', methods=['GET', 'POST'])
def add_statement():
    """Route for adding statements"""
    form = StatementsForm()
    if form.validate_on_submit():
        try:
            statement = Statements(
                name=form.name.data,
                document=form.document.data.read(),  # Read file data for document
                date=form.date.data,
                status=form.status.data,
                created_at=datetime.utcnow()
            )
            db_storage.new(statement)
            db_storage.save()
            flash('Statement has been created!', 'success')
            logger.info(f'Statement "{statement.name}" created successfully.')
            return redirect(url_for('legislation.add_statement'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f'Error creating statement: {str(e)}')
    return render_template('add_statement.html', title='Add Statement', form=form)

@legislation_bp.route('/view_statements', methods=['GET'])
def view_statements():
    statements_dict = db_storage.all(Statements)
    statements = list(statements_dict.values())
    return render_template('view_statements.html', title='View Statements', statements=statements)

#create function to edit statements
@legislation_bp.route('/edit_statement/<int:statement_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_statement(statement_id):
    statement = db_storage.get(Statements, id=statement_id)
    form = StatementsForm(obj=statement)
    if form.validate_on_submit():
        try:
            statement.name = form.name.data
            statement.date = form.date.data
            statement.status = form.status.data
            if form.document.data:
                statement.document = form.document.data.read()
            db_storage.save()
            flash('Statement has been updated!', 'success')
            return redirect(url_for('legislation.view_statements'))
        except Exception as e:
            logging.error(f"Error editing statement: {e}")
            flash('An error occurred while editing the statement. Please try again.', 'danger')
    return render_template('edit_statement.html', title='Edit Statement', form=form, statement=statement)

#create function to delete statements
@legislation_bp.route('/delete_statement/<int:statement_id>', methods=['POST'], strict_slashes=False)
def delete_statement(statement_id):
    statement = db_storage.get(Statements, id=statement_id)
    db_storage.delete(statement)
    db_storage.save()
    flash('Statement has been deleted!', 'success')
    return redirect(url_for('legislation.view_statements'))



@legislation_bp.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    """route for the questions"""
    return render_template('view_questions.html', title='Questions')

@legislation_bp.route('/add_question', methods=['GET', 'POST'])
def add_question():
    form = QuestionsForm()
    if form.validate_on_submit():
        file_data = form.document.data.read() if form.document.data else None
        
        new_question = Questions(
            name=form.name.data,
            document=file_data,
            date=form.date.data,
            status=form.status.data,
            created_at=datetime.utcnow()
        )
        try:
            db_storage.new(new_question)
            db_storage.save()  # Commit the session to save the new question
            flash('Question added successfully!', 'success')
            return redirect(url_for('legislation.view_questions'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    return render_template('add_question.html', form=form)

#create route to view questions
@legislation_bp.route('/view_questions', methods=['GET', 'POST'])
def view_questions():
    questions_dict = db_storage.all(Questions)
    questions = list(questions_dict.values())
    return render_template('view_questions.html', title='View Questions', questions=questions)

@legislation_bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_question(question_id):
    question = db_storage.get(Questions, id=question_id)
    form = QuestionsForm(obj=question)
    if form.validate_on_submit():
        try:
            question.name = form.name.data
            question.date = form.date.data
            question.status = form.status.data
            if form.document.data:
                question.document = form.document.data.read()
            db_storage.save()
            flash('Question has been updated!', 'success')
            return redirect(url_for('legislation.view_questions'))
        except Exception as e:
            logging.error(f"Error editing statement: {e}")
            flash('An error occurred while editing the question. Please try again.', 'danger')
    return render_template('edit_question.html', title='Edit Question', form=form, question=question)

#create function to delete statements
@legislation_bp.route('/delete_question/<int:question_id>', methods=['POST'], strict_slashes=False)
def delete_question(question_id):
    question = db_storage.get(Questions, id=question_id)
    db_storage.delete(question)
    db_storage.save()
    flash('Question has been deleted!', 'success')
    return redirect(url_for('legislation.view_questions'))


#create a route for functions
@legislation_bp.route('/functions', methods=['GET', 'POST'])
def functions():
    """route for the functions"""
    return render_template('functions.html', title='Functions')

@legislation_bp.route('/download_motion/<int:motion_id>', methods=['GET'])
def download_motion(motion_id):
    """Route to download a motion."""
    try:
        motion = db_storage.get(Motions, id=motion_id)
        if not motion:
            flash(f'Motion with ID {motion_id} not found.', 'error')
            return redirect(url_for('legislation.view_motions'))

        return send_file(BytesIO(motion.document), as_attachment=True, download_name=f'motion_{motion_id}.pdf')

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the motion: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the motion: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

@legislation_bp.route('/download_statement/<int:statement_id>', methods=['GET'])
def download_statement(statement_id):
    """Route to download a statement."""
    try:
        statement = db_storage.get(Statements, id=statement_id)
        if not statement:
            flash(f'Statement with ID {statement_id} not found.', 'error')
            return redirect(url_for('legislation.view_statements'))

        return send_file(BytesIO(statement.document), as_attachment=True, download_name=f'statement_{statement_id}.pdf')

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the statement: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the statement: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))

@legislation_bp.route('/download_question/<int:question_id>', methods=['GET'])
def download_question(question_id):
    """Route to download a question."""
    try:
        question = db_storage.get(Questions, id=question_id)
        if not question:
            flash(f'Question with ID {question_id} not found.', 'error')
            return redirect(url_for('legislation.view_questions'))

        return send_file(BytesIO(question.document), as_attachment=True, download_name=f'question_{question_id}.pdf')

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the question: {e}', 'error')
        return redirect(url_for('legislation.view_questions'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the question: {e}', 'error')
        return redirect(url_for('legislation.view_questions'))