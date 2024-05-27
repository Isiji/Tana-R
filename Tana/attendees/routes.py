#!/usr/bin/python3
"""Routes for the attendees"""
from flask import Blueprint, jsonify, request
from flask import render_template, redirect, url_for, flash
from Tana.models.attendees import Attendees
from Tana.attendees.forms import AttendeesForm, UpdateAttendeesForm, DeleteAttendeesForm, SearchAttendeesForm
from Tana.engine.storage import DBStorage

attendees = Blueprint('attendees', __name__)

@attendees.route('/attendees', methods=['GET', 'POST'])
def attendees():
    """attendees route"""
    return render_template('attendees.html')

