#!/usr/bin/python3
"""routes for the human resource"""

from flask import Blueprint, request
from flask import render_template, redirect, url_for, flash, jsonify
from Tana.models.humanresource import HumanResource

humanresource = Blueprint('humanresource', __name__)
