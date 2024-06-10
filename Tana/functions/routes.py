#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from Tana.models.funcategory import FunctionCategory
from Tana.models.functions import Functions

functions_bp = Blueprint('functions', __name__)
@functions_bp.route('/functions', methods=['GET'])
def functions():
    """Get all functions"""
    return render_template('functions.html')


