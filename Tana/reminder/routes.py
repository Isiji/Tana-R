#!/usr/bin/python3
"""Routes for the reminders"""
from flask import Blueprint, jsonify, request
from flask import render_template, redirect, url_for, flash
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm, UpdateReminderForm, DeleteReminderForm, ReminderSearchForm
from Tana.engine.storage import DBStorage


reminders = Blueprint('reminders', __name__)

