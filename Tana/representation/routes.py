import logging
from flask import Blueprint, current_app, render_template, request, flash, jsonify, redirect, url_for
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana import db_storage
import pandas as pd
import os
import csv

representation = Blueprint('representation', __name__)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@representation.route('/pollingstations', methods=['GET'])
def view_results():
    constituencies = db_storage.all(Constituency).values()
    wards = db_storage.all(Ward).values()
    polling_stations = db_storage.all(PollingStation).values()
    return render_template('results.html', title='Results', constituencies=constituencies, wards=wards, polling_stations=polling_stations)

@representation.route('/polling_station_form')
def polling_station_form():
    return render_template('polling_station_form.html')

@representation.route('/get_polling_station_info')
def get_polling_station_info():
    polling_station_name = request.args.get('polling_station')
    polling_station = db_storage.get_pollingstation_by_name(polling_station_name)
    if polling_station:
        ward = db_storage.get_ward_by_id(polling_station.ward_id)
        constituency = db_storage.get_constituency_by_id(ward.constituency_id)
        return jsonify({
            'ward': ward.name,
            'constituency': constituency.name
        })
    else:
        return jsonify({
            'ward': '',
            'constituency': ''
        }), 404