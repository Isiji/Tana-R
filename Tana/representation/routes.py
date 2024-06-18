#!/usr/bin/python3
"""routes for the representation"""
from flask import Blueprint,jsonify, render_template, request, redirect, url_for, flash
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.models.pollingstation import PollingStation

representation = Blueprint('representation', __name__)

@representation.route('/representation', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def representation_dashboard():
    """route for the representation dashboard"""
    return render_template('representation.html', title='representation Dashboard')

@representation.route('/get_wards_and_constituency', methods=['GET', 'POST'], strict_slashes=False)
def get_wards_and_constituency():
    """route for getting wards and constituency"""
    polling_station_name = request.args.get('polling_station_name')
    polling_station = db_storage.get(PollingStation, id=polling_station_name)

    if polling_station:
        ward = polling_station.village.ward
        constituency = ward.constituency

        return jsonify({'ward': ward.name, 'constituency': constituency.name})
    else:
        return jsonify({'success': False, 'message': 'Polling station not found'})
    
