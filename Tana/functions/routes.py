#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request
from Tana.models.funcategory import FunctionCategory
from Tana.models.functions import Functions

functions = Blueprint('functions', __name__)
