#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request
from Tana.models.funcategory import FunctionCategory

main = Blueprint('main', __name__)